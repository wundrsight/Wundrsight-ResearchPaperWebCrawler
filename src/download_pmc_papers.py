# src/download_pmc_papers.py

import os
import requests
from xml.etree import ElementTree
import logging

# Configure logging
logging.basicConfig(
    filename='download_pmc_papers.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def fetch_pmc_ids(query, max_results=10):
    """
    Fetch PMC IDs from PubMed based on the query.

    :param query: Search query.
    :param max_results: Maximum number of results to fetch.
    :return: List of PMC IDs.
    """
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pmc',
            'term': query,
            'retmax': max_results,
            'retmode': 'xml'
        }
        response = requests.get( base_url, params=params )
        if response.status_code == 200:
            root = ElementTree.fromstring( response.content )
            pmc_ids = [id_elem.text for id_elem in root.findall( './/Id' )]
            logging.info( f"Fetched {len( pmc_ids )} PMC IDs." )
            return pmc_ids
        else:
            logging.error( f"Error fetching PMC IDs: {response.status_code}" )
            print( f"Error fetching PMC IDs: {response.status_code}" )
            return []
    except Exception as e:
        logging.error( f"Exception in fetch_pmc_ids: {e}" )
        print( f"Exception in fetch_pmc_ids: {e}" )
        return []


def get_pmc_pdf_url(pmc_id):
    """
    Construct the PDF download URL from PMC ID.

    :param pmc_id: PubMed Central ID.
    :return: URL to download the PDF.
    """
    return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"


def download_pdf(pdf_url, identifier, save_dir='../data/pmc_pdfs'):
    """
    Download PDF from the given URL and save it to the specified directory.

    :param pdf_url: URL of the PDF to download.
    :param identifier: Unique identifier for the paper (e.g., PMC ID).
    :param save_dir: Directory to save the downloaded PDF.
    :return: Local file path to the downloaded PDF or None if failed.
    """
    try:
        if not os.path.exists( save_dir ):
            os.makedirs( save_dir )
            logging.info( f"Created directory: {save_dir}" )
            print( f"Created directory: {save_dir}" )

        # Sanitize the identifier for filename
        filename = f"{identifier}.pdf"
        filepath = os.path.join( save_dir, filename )

        # Check if the PDF already exists
        if os.path.exists( filepath ):
            logging.info( f"PDF already exists for: {identifier}" )
            print( f"PDF already exists for: {identifier}" )
            return filepath

        response = requests.get( pdf_url, stream=True )
        response.raise_for_status()

        with open( filepath, 'wb' ) as f:
            for chunk in response.iter_content( 1024 ):
                if chunk:
                    f.write( chunk )

        logging.info( f"Downloaded PDF for: {identifier}" )
        print( f"Downloaded PDF for: {identifier}" )
        return filepath

    except requests.exceptions.RequestException as e:
        logging.error( f"Failed to download PDF for {identifier}: {e}" )
        print( f"Failed to download PDF for {identifier}: {e}" )
        return None
