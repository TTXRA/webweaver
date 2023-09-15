from bs4 import BeautifulSoup
from SaveMongo import save
import requests


def ww_els(query, query_type="0", query_date="0"):
    # Replace spaces in the 'query' string with '+' to create a URL-friendly format
    query = query.replace(' ', '+')

    # Define a dictionary to map user input to query types
    query_type_map = {
        "1": "TITLE",
        "2": "AUTH",
        "3": "SRCTITLE",
        "4": "KEY",
    }

    # Use dictionary.get() to handle invalid input gracefully
    query_type = query_type_map.get(query_type, "all")

    # Define HTTP request headers with API key and institutional token
    header = {
        "Accept": "application/xml",
        "X-ELS-APIKey": "9589b3fbd9c2dc9ae80c650da5b29fdf",
        "X-ELS-Insttoken": "721db35f2394414657e9c7e9bd9e4695"
    }

    # Construct the API URL with the query parameter
    if query_date != "0":
        api_url = f"https://api.elsevier.com/content/search/scopus?query={query_type}({query})&date={query_date}"
    else:
        api_url = f"https://api.elsevier.com/content/search/scopus?query={query_type}({query})"

    # Send an HTTP GET request to the API
    response = requests.get(api_url, headers=header)

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
        save(adapted_entries, query, query_date, total, "els")
    else:
        print("Nenhum resultado no SCOPUS para a consulta em questão.")


# Function to adapt individual 'entry' elements from JSON to a dictionary
def adapt_entry(entry):
    # Extract affiliation data and format it
    affilname = entry.find("atom:affilname").text if entry.find("atom:affilname") else ""
    affiliation_city = entry.find("atom:affiliation-city").text if entry.find("atom:affiliation-city") else ""
    affiliation_country = entry.find("atom:affiliation-country").text if entry.find("affiliation-country") else ""

    affiliation = f"{affilname}, {affiliation_city}, {affiliation_country}" if entry.find("atom:affiliation") else ""

    # Create an adapted entry dictionary with selected fields
    adapted_entry = {
        "title": entry.find("dc:title").text.upper(),
        "authors": entry.find("dc:creator").text if entry.find("dc:creator") else "",
        "originalId": entry.find("dc:identifier").text,
        "url": entry.find("prism:url").text,
        "doi": entry.find("prism:doi").text if entry.find("prism:doi") else "",
        "issn": entry.find("prism:issn").text if entry.find("prism:issn") else "",
        "date": entry.find("prism:coverDisplayDate").text,
        "source": entry.find("prism:publicationName").text,
        "volume": entry.find("prism:volume").text if entry.find("prism:volume") else "",
        "pageRange": entry.find("prism:pageRange").text if entry.find("prism:pageRange") else "",
        "type": entry.find("atom:subtypeDescription").text,
        "affiliation": affiliation,
    }
    return adapted_entry
