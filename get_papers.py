
import requests
import xml.etree.ElementTree as ET
import re
import csv

def fetch_papers(query, debug=False):
    """Fetch papers from PubMed based on the query."""
    if debug:
        print(f"Fetching papers for query: {query}")

    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": 100,
        "retmode": "json"
    }
    response = requests.get(search_url, params=search_params)
    response.raise_for_status()
    paper_ids = response.json()["esearchresult"]["idlist"]

    if debug:
        print(f"Retrieved Paper IDs: {paper_ids}")

    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }
    details = requests.get(fetch_url, params=fetch_params)
    details.raise_for_status()

    return details.text

def parse_papers(xml_data, debug=False):
    """Parse XML data to extract required paper information."""
    if debug:
        print("Parsing XML data...")

    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.find(".//PMID").text or "N/A"
        title = article.find(".//ArticleTitle").text or "N/A"
        pub_date = article.find(".//PubDate/Year").text or "N/A"

        # Debugging for missing fields
        if pubmed_id == "N/A":
            print("Missing PubMed ID for an article")
        if title == "N/A":
            print(f"Missing title for PubMed ID {pubmed_id}")
        if pub_date == "N/A":
            print(f"Missing publication date for PubMed ID {pubmed_id}")

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None

        # Extract authors and affiliations
        for author in article.findall(".//Author"):
            affiliation = author.find(".//Affiliation")
            affiliation_text = affiliation.text if affiliation is not None else "None"  # Safe access to text
            
            last_name = author.find("LastName")
            last_name_text = last_name.text if last_name is not None else "Unknown"  # Safe access to text

            if debug:
                print(f"Author: {last_name_text}, Affiliation: {affiliation_text}")

            # Check for non-academic author (e.g., from companies or pharma-related affiliations)
            if re.search(r"(Inc|Ltd|Pharma|Biotech|Corporation|Company|Industry|Labs|LLC|Co\.?)", affiliation_text, re.IGNORECASE):
                non_academic_authors.append(last_name_text)
                company_affiliations.append(affiliation_text)

        # Debugging: Check structure of each author for email
        if debug:
            print(f"Checking for email in article with PubMed ID: {pubmed_id}")


        # Extract corresponding author email
        for affiliation_info in article.findall(".//AffiliationInfo/Affiliation"):
            if affiliation_info is not None and affiliation_info.text:
                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", affiliation_info.text)
                if email_match:
                    corresponding_email = email_match.group()
                    break

        # If email wasn't found in AffiliationInfo, check the author section for <Email> element (common in PubMed articles)
        if corresponding_email is None:
            for author in article.findall(".//Author"):
                email = author.find("Email")
                if email is not None and email.text:
                    corresponding_email = email.text
                    if debug:
                        print(f"Found email from Author section: {corresponding_email}")
                    break


        papers.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email or "N/A"
        })

    return papers




def save_to_csv(data, filename):
    """Save the paper data to a CSV file."""
    if data:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Results saved to {filename}")
    else:
        print("No data to save.")


# Example of running the script
if __name__ == "__main__":
    query = "cancer treatment"  # Replace with your query
    xml_data = fetch_papers(query, debug=True)
    papers = parse_papers(xml_data, debug=True)
    save_to_csv(papers, r'D:\results.csv')





