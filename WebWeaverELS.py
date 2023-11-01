from bs4 import BeautifulSoup
from SaveMongo import save
import requests


def ww_els(query, query_type, query_date, query_id):
    # Replace spaces in the 'query' string with '+' to create a URL-friendly format
    query = query.replace(' ', '+')

    match query_type:
        case "1":
            query_type = "TITLE"
        case "2":
            query_type = "AUTH"
        case "3":
            query_type = "SRCTITLE"
        case "4":
            query_type = "KEY"
        case _:
            query_type = "all"

    # Construct the API URL with the query parameter
    if query_date != "":
        api_url = f"https://api.elsevier.com/content/search/scopus?query={query_type}({query})&date={query_date}"
    else:
        api_url = f"https://api.elsevier.com/content/search/scopus?query={query_type}({query})"

    # Define HTTP request headers with API key and institutional token
    header = {
        "Accept": "application/xml",
        "X-ELS-APIKey": "9589b3fbd9c2dc9ae80c650da5b29fdf",
        "X-ELS-Insttoken": "721db35f2394414657e9c7e9bd9e4695"
    }

    # Send an HTTP GET request to the API
    response = requests.get(api_url, headers=header)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response using BeautifulSoup
        soup = BeautifulSoup(response.content, "xml")

        # Find the 'opensearch:totalResults' element in the 'soup' object and extract its numeric content
        # The result is stored in the 'total' variable as a string of digits
        total = "".join(filter(str.isdigit, soup.find("opensearch:totalResults")))

        if total != "0":
            # Convert XML to JSON
            entries = soup.find_all("atom:entry")

            # Create an empty list to store the adapted entries
            adapted_entries = []

            # Loop through each original entry and adapt it
            for entry in entries:
                adapted_entry = adapt_entry(entry)
                adapted_entries.append(adapted_entry)

            # Call the function to save the data to MongoDB
            save(adapted_entries, query, query_date, query_id, total, "els")
        else:
            print("Nenhum resultado no SCOPUS para a consulta em questão.")
    else:
        total = 0
        print("A requisição enviada à API do SCOPUS não foi atendida.")

    return total


# Function to adapt individual 'entry' elements from JSON to a dictionary
def adapt_entry(entry):
    # Extract affiliation data and format it
    affilname = entry.find("atom:affilname").text if entry.find("atom:affilname") else ""
    affiliation_city = entry.find("atom:affiliation-city").text if entry.find("atom:affiliation-city") else ""
    affiliation_country = entry.find("atom:affiliation-country").text if entry.find("affiliation-country") else ""
    affiliation = f"{affilname}, {affiliation_city}, {affiliation_country}" if entry.find("atom:affiliation") else "N/A"

    # Create an adapted entry dictionary with selected fields
    adapted_entry = {
        "title": entry.find("dc:title").text.upper(),
        "authors": entry.find("dc:creator").text.upper() if entry.find("dc:creator") else "N/A",
        "database": "SCOPUS",
        "originalId": entry.find("dc:identifier").text.upper(),
        "url": entry.find("prism:url").text.upper(),
        "doi": entry.find("prism:doi").text.upper() if entry.find("prism:doi") else "N/A",
        "issn": entry.find("prism:issn").text.upper() if entry.find("prism:issn") else "N/A",
        "date": entry.find("prism:coverDisplayDate").text.upper(),
        "source": entry.find("prism:publicationName").text.upper(),
        "volume": entry.find("prism:volume").text.upper() if entry.find("prism:volume") else "N/A",
        "pageRange": entry.find("prism:pageRange").text.upper() if entry.find("prism:pageRange") else "N/A",
        "type": entry.find("atom:subtypeDescription").text.upper(),
        "affiliation": affiliation.upper(),
    }

    return adapted_entry
