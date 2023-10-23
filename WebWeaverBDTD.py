from bs4 import BeautifulSoup
from SaveMongo import save
import requests
import re


def ww_bdtd(query, query_type, query_date, query_id):
    # Replace spaces in the query with '+' to create a valid URL parameter
    query = query.replace(' ', '+')

    match query_type:
        case "1":
            query_type = "Title"
        case "2":
            query_type = "Author"
        case "3":
            query_type = "Subject"
        case _:
            query_type = "AllFields"

    # Set a limit for the number of results to retrieve
    limit = 25

    # Construct the API URL with the query and limit parameters
    if query_date != "":
        url = f"https://bdtd.ibict.br/vufind/api/v1/search?filter%5B%5D=publishDate%3A%22%5B{query_date}+TO+{query_date}%5D%22&join=AND&bool0%5B%5D=AND&lookfor0%5B%5D={query}&type0%5B%5D={query_type}&limit={limit}&file=true"
    else:
        url = f"https://bdtd.ibict.br/vufind/api/v1/search?lookfor={query}&type={query_type}&limit={limit}&file=true"

    # Send an HTTP GET request to the API and store the response
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Use regular expression to find and extract the total number of results
    total = re.search(r'\d+', response.text)

    if total.group() != "0":
        # Parse the JSON data from the response
        data = response.json()

        # Extract the list of records from the JSON data
        records = data.get("records", [])

        # Create an empty list to store the adapted records
        adapted_records = []

        # Loop through each original record and adapt it
        for record in records:
            adapted_record = adapt_record(record)
            adapted_records.append(adapted_record)

        # Call the function to save the data to MongoDB
        save(adapted_records, query, query_date, query_id, total.group(), "bdtd")
    else:
        print("Nenhum resultado na BDTD para a consulta em questão.")

    return total.group()


# Function to adapt individual 'record' elements from JSON to a dictionary
def adapt_record(record):
    advisor_key = record.get("contributors", {}).get("advisor")
    advisor = list(advisor_key.keys())[0].title() if advisor_key else "N/A"
    institutions = ", ".join(record["institutions"])
    department = ", ".join(record.get("departments", []))

    # Include department only if it exists
    if department:
        combined_institution = f"{institutions}, {department}"
    else:
        combined_institution = institutions

    # Create an adapted record dictionary with selected fields
    adapted_record = {
        "title": record["title"].upper(),
        "authors": "; ".join(author.rstrip('.').upper() for author in record["authors"]["primary"]),
        "database": "Biblioteca Digital Brasileira de Teses e Dissertações".upper(),
        "originalId": record["id"].upper(),
        "url": record["urls"][0].upper() if record["urls"] else "N/A",
        "date": record["publicationDates"][0].upper() if record["publicationDates"] else "N/A",
        "affiliation": combined_institution.upper(),
        "advisor": advisor.upper(),
        "type": ", ".join(typ.upper() for typ in record["types"]),
        "keywords": "; ".join(subject[0].replace(";", "").upper() for subject in record.get("subjectsPOR", [])),
    }
    return adapted_record
