from SaveMongo import save
import requests
import re


def ww_wos(query, query_type="0", query_date="0"):
    # Replace spaces in the 'query' string with '+' to create a URL-friendly format
    query = query.replace(' ', '+')

    # Define a dictionary to map user input to query types
    query_type_map = {
        "1": "TI",
        "2": "AU",
        "3": "SO",
        "4": "KEY",
    }

    # Use dictionary.get() to handle invalid input gracefully
    query_type = query_type_map.get(query_type, "TS")

    # Set the number of results to retrieve and the initial page
    limit = 25
    page = 1

    # Construct the API URL with the query, limit, and page parameters
    if query_date != "0":
        url = f"https://api.clarivate.com/apis/wos-starter/v1/documents?db=WOS&q=PY%3D{query_date}%20AND%20{query_type}%3D{query}&limit={limit}&page={page}"
    else:
        url = f"https://api.clarivate.com/apis/wos-starter/v1/documents?db=WOS&q={query_type}%3D{query}&limit={limit}&page={page}"

    # Define the headers for the HTTP request
    headers = {
        "X-ApiKey": "75982a59b8cf5595cf4d74c231af3b82e65625cc"
    }

    # Send an HTTP GET request to the API
    response = requests.get(url, headers=headers)

    # Use regular expression to search for the first sequence of digits (numbers) in the response text
    total = re.search(r'\d+', response.text)

    if total.group() != "0":
        # Parse the JSON data from the response
        data = response.json()

        # Extract the list of hits from the data
        hits = data.get("hits", [])

        # Create an empty list to store the adapted hits
        adapted_hits = []

        # Loop through each original hit and adapt it
        for hit in hits:
            adapted_hit = adapt_hit(hit)
            adapted_hits.append(adapted_hit)

        # Call the function to save the data to MongoDB
        save(adapted_hits, query, query_date, total.group(), "wos")
    else:
        print("Nenhum resultado no Web of Science para a consulta em questão.")


# Function to adapt individual 'hit' elements from JSON to a dictionary
def adapt_hit(hit):
    publish_year = hit['source']['publishYear']
    publish_month = hit['source'].get('publishMonth', None)

    if publish_month is not None:
        # Create a formatted date string with year and capitalized month
        date = f"{publish_year}, {publish_month.capitalize()}"
    else:
        date = str(publish_year)

    # Initialize the 'authors' variable as an empty string
    authors = ""
    if "names" in hit and "authors" in hit["names"]:
        # Check if the 'authors' key exists in 'hit["names"]'
        authors = "; ".join(author["wosStandard"] for author in hit["names"]["authors"])

    # Create an adapted hit dictionary with selected fields
    adapted_hit = {
        "title": hit["title"],
        "authors": authors,
        "originalId": hit["uid"],
        "url": hit["links"]["record"],
        "doi": hit["identifiers"].get("doi", "N/A"),
        "issn": hit["identifiers"].get("issn", "N/A"),
        "date": date,
        "source": hit["source"]["sourceTitle"],
        "volume": hit["source"].get("volume", "N/A"),
        "pageRange": hit["source"]["pages"].get("range", "N/A"),
        "type": ", ".join(hit["types"]),
        "keywords": "; ".join(keyword for keyword in hit["keywords"].get("authorKeywords", [])),
    }
    return adapted_hit