from SaveMongo import save
import requests
import re


def ww_wos(query, query_type, query_date, query_id):
    # Replace spaces in the 'query' string with '+' to create a URL-friendly format
    query = query.replace(' ', '+')

    match query_type:
        case "1":
            query_type = "TI"
        case "2":
            query_type = "AU"
        case "3":
            query_type = "SO"
        case "4":
            query_type = "KEY"
        case _:
            query_type = "TS"

    # Set the number of results to retrieve and the initial page
    limit = 25
    page = 1

    # Construct the API URL with the query, limit, and page parameters
    if query_date != "":
        url = f"https://api.clarivate.com/apis/wos-starter/v1/documents?db=WOS&q=PY%3D{query_date}%20AND%20{query_type}%3D{query}&limit={limit}&page={page}"
    else:
        url = f"https://api.clarivate.com/apis/wos-starter/v1/documents?db=WOS&q={query_type}%3D{query}&limit={limit}&page={page}"

    # Define the headers for the HTTP request
    headers = {
        "X-ApiKey": ""
    }

    # Send an HTTP GET request to the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Use regular expression to search for the first sequence of digits (numbers) in the response text
        total = re.search(r'\d+', response.text)
        total = total.group()

        if total != "0":
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
            save(adapted_hits, query, query_date, query_id, total, "wos")
        else:
            print("Nenhum resultado no Web of Science para a consulta em questão.")
    else:
        total = 0
        print("A requisição enviada à API do Web of Science não foi atendida.")

    return total


# Function to adapt individual 'hit' elements from JSON to a dictionary
def adapt_hit(hit):
    publish_year = hit['source']['publishYear']
    publish_month = hit['source'].get('publishMonth', None)

    if publish_month is not None:
        # Create a formatted date string with year and capitalized month
        date = f"{publish_month} {publish_year}"
    else:
        date = str(publish_year)

    # Initialize the 'authors' variable as an empty string
    authors = ""
    if "names" in hit and "authors" in hit["names"]:
        # Check if the 'authors' key exists in 'hit["names"]'
        authors = "; ".join(author["wosStandard"] for author in hit["names"]["authors"])

    # Create an adapted hit dictionary with selected fields
    adapted_hit = {
        "title": hit["title"].upper(),
        "authors": authors.upper(),
        "database": "WEB OF SCIENCE",
        "originalId": hit["uid"].upper(),
        "url": hit["links"]["record"].upper(),
        "doi": hit["identifiers"].get("doi", "N/A").upper(),
        "issn": hit["identifiers"].get("issn", "N/A").upper(),
        "date": date.upper(),
        "source": hit["source"]["sourceTitle"].upper(),
        "volume": hit["source"].get("volume", "N/A").upper(),
        "pageRange": hit["source"]["pages"].get("range", "N/A").upper(),
        "type": ", ".join(hit["types"]).upper(),
        "keywords": "; ".join(keyword.upper() for keyword in hit["keywords"].get("authorKeywords", ["N/A"]))
    }
    return adapted_hit
