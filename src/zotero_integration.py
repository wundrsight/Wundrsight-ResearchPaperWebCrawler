# src/zotero_integration.py

import requests
import logging
from database_setup import session, Paper
import os

# Configure logging
logging.basicConfig(
    filename='zotero_integration.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

ZOTERO_API_KEY = os.getenv('ZOTERO_API_KEY')
ZOTERO_LIBRARY_ID = os.getenv('ZOTERO_LIBRARY_ID')
ZOTERO_LIBRARY_TYPE = os.getenv('ZOTERO_LIBRARY_TYPE', 'user')  # 'user' or 'group'

def add_all_to_zotero():
    """
    Add all papers in the database to Zotero.
    """
    if not ZOTERO_API_KEY or not ZOTERO_LIBRARY_ID:
        print("Zotero API credentials not set.")
        logging.error("Zotero API credentials not set.")
        return

    headers = {
        'Zotero-API-Key': ZOTERO_API_KEY,
        'Content-Type': 'application/json'
    }

    # Construct the Zotero library URL
    url = f"https://api.zotero.org/{ZOTERO_LIBRARY_TYPE}/{ZOTERO_LIBRARY_ID}/items"

    papers = session.query(Paper).all()
    for paper in papers:
        # Skip if already added to Zotero (optional: implement a flag or check)
        # Here, we'll attempt to add all papers regardless
        item = {
            "itemType": "journalArticle",
            "title": paper.title,
            "creators": [{"creatorType": "author", "firstName": author.split(' ')[0], "lastName": ' '.join(author.split(' ')[1:])} for author in paper.authors.split(',')],
            "publicationTitle": "",  # Optional: Add if available
            "date": str(paper.year) if paper.year else "",
            "DOI": paper.doi if paper.doi else "",
            "abstractNote": paper.abstract if paper.abstract else "",
            "url": paper.pdf_path if paper.pdf_path else ""
        }

        try:
            response = requests.post(url, headers=headers, json=item)
            if response.status_code in [200, 201]:
                print(f"Added to Zotero: {paper.title}")
                logging.info(f"Added to Zotero: {paper.title}")
            else:
                print(f"Failed to add to Zotero: {paper.title}. Status Code: {response.status_code}")
                logging.error(f"Failed to add to Zotero: {paper.title}. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Exception while adding to Zotero: {paper.title}. Error: {e}")
            logging.error(f"Exception while adding to Zotero: {paper.title}. Error: {e}")
