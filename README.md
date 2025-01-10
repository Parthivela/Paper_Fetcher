PubMed Research Paper Fetcher
Project Description
This Python program fetches research papers from PubMed based on a user-provided query. It filters the results to include papers where at least one author is affiliated with pharmaceutical or biotech companies. The results are then saved to a CSV file with relevant details such as title, authors, publication date, and affiliations.

Features
Fetch research papers from PubMed using an API query.
Filter papers based on author affiliation with pharmaceutical or biotech companies.
Save filtered results to a CSV file with titles, authors, publication date, and affiliations.
Requirements
Python 3.x
requests library (for making HTTP requests)
argparse library (for handling command-line arguments)
csv library (for writing data to a CSV file)

CSV Output Format
The output CSV file will contain the following columns:

Title: Title of the research paper.
Authors: List of authors who contributed to the paper.
Publication Date: The date the paper was published.
Affiliation: Affiliations of the authors, specifically looking for pharmaceutical or biotech affiliations.
