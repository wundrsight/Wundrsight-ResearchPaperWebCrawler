# src/fetch_papers.py

import requests
import logging
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_papers(query, limit=20, fields="title,authors,year,abstract,citationCount,externalIds,openAccessPdf"):
    """
    Fetch papers from Semantic Scholar based on the search query.

    :param query: The search query string.
    :param limit: Number of results to fetch.
    :param fields: Comma-separated string of fields to retrieve.
    :return: List of paper dictionaries.
    """
    try:
        params = {
            "query": query,
            "limit": limit,
            "fields": fields,
            "sort": "year",            # Sort by year to get recent papers
            "order": "desc"            # Descending order
        }
        headers = {
            "Accept": "application/json",
            "x-api-key": os.getenv('SEMANTIC_SCHOLAR_API_KEY')  # Use your API key from .env
        }

        logger.info(f"Fetching papers with query: '{query}', limit: {limit}")

        response = requests.get(SEMANTIC_SCHOLAR_API_URL, params=params, headers=headers)

        logger.debug(f"Request URL: {response.url}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 200:
            data = response.json()
            papers = data.get('data', [])
            logger.info(f"Successfully fetched {len(papers)} papers.")
            return papers
        else:
            logger.error(f"Error fetching papers from Semantic Scholar: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        logger.error(f"Exception occurred while fetching papers: {e}")
        return []
