# src/app.py

import os
from fetch_papers import fetch_papers
from download_arxiv_papers import fetch_arxiv_papers, download_pdf as download_arxiv_pdf
from download_unpaywall_papers import get_unpaywall_pdf, download_pdf as download_oa_pdf
from download_pmc_papers import fetch_pmc_ids, get_pmc_pdf_url, download_pdf as download_pmc_pdf
from download_doaj_papers import search_doaj, download_doaj_pdf
from store_papers import store_papers
from categorize_papers import categorize_papers  # Corrected comment syntax
from zotero_integration import add_all_to_zotero
from dotenv import load_dotenv
from database_setup import setup_database, Paper, session  # Adjusted import

# Load environment variables
load_dotenv()

def main():
    # Initialize the database and get the session
    session = setup_database()
    if not session:
        print("Failed to initialize the database. Exiting.")
        return

    # Example usage: Fetch, download, store, categorize, and integrate with Zotero
    query = "AI in VR mental health"
    max_results = 10

    # Fetch papers from arXiv
    print("Fetching papers from arXiv...")
    arxiv_papers = fetch_arxiv_papers(query, max_results=max_results)

    # Attempt to fetch PDFs via Unpaywall if not available from arXiv
    for paper in arxiv_papers:
        if not paper.get('pdf_url') and paper.get('doi'):
            print(f"Attempting to fetch PDF via Unpaywall for DOI: {paper['doi']}")
            oa_pdf_url = get_unpaywall_pdf(paper['doi'])
            if oa_pdf_url:
                paper['pdf_url'] = oa_pdf_url
            else:
                print(f"No OA PDF found for DOI: {paper['doi']}")

    # Store papers and download PDFs
    print("Storing papers and downloading PDFs...")
    store_papers(arxiv_papers, session)

    # Categorize papers
    print("Categorizing papers...")
    categorize_papers(session, threshold=50)

    # Integrate with Zotero
    print("Integrating with Zotero...")
    add_all_to_zotero(session)

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
