# src/integrated_download.py

import logging
from fetch_papers import fetch_papers
from download_papers import download_pdf
from store_papers import store_papers
from categorize_papers import categorize_papers
from zotero_integration import add_all_to_zotero
from database_setup import session, Paper
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def integrated_download(query, email, max_results=5):
    """
    Integrated download from multiple sources based on the search query.

    :param query: The search query string.
    :param email: User's email for Unpaywall API.
    :param max_results: Maximum number of results to fetch per source.
    """
    try:
        logger.info("Starting integrated download process...")

        # Step 1: Fetch papers from Semantic Scholar
        logger.info("Fetching papers from Semantic Scholar...")
        semantic_papers = fetch_papers(query, limit=max_results)
        if not semantic_papers:
            logger.warning("No papers fetched from Semantic Scholar.")

        # Step 2: Store fetched papers
        logger.info("Storing fetched papers...")
        store_papers(semantic_papers)

        # Step 3: Categorize papers
        logger.info("Categorizing papers...")
        categorize_papers(threshold=50)

        # Step 4: Add papers to Zotero

        logger.info("Integrated download process completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during the integrated download process: {e}")
        raise e  # Propagate the exception to be handled by the caller
