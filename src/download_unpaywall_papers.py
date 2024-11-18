# src/download_unpaywall_papers.py

import os
import requests
import logging

# Configure logging
logging.basicConfig(
    filename='download_unpaywall_papers.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def get_unpaywall_pdf(doi, email):
    """
    Get OA PDF link from Unpaywall using DOI.

    :param doi: Digital Object Identifier of the paper.
    :param email: Your email address (required by Unpaywall for contact purposes).
    :return: URL of the OA PDF if available, else None.
    """
    try:
        url = f"https://api.unpaywall.org/v2/{doi}"
        params = {
            'email': email  # Unpaywall requires an email for contact purposes
        }
        response = requests.get( url, params=params )
        if response.status_code == 200:
            data = response.json()
            if data.get( 'is_oa' ) and data.get( 'best_oa_location' ) and data['best_oa_location'].get( 'url_for_pdf' ):
                logging.info( f"Found OA PDF for DOI: {doi}" )
                return data['best_oa_location']['url_for_pdf']
        logging.info( f"No OA PDF found for DOI: {doi}" )
        return None
    except Exception as e:
        logging.error( f"Exception in get_unpaywall_pdf for DOI {doi}: {e}" )
        return None


def download_pdf(pdf_url, identifier, save_dir='../data/oa_pdfs'):
    """
    Download PDF from the given URL and save it to the specified directory.

    :param pdf_url: URL of the PDF to download.
    :param identifier: Unique identifier for the paper (e.g., title, DOI).
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
