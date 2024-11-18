# src/download_papers.py

import requests
import os
import logging

# Configure logging
logging.basicConfig( level=logging.DEBUG )
logger = logging.getLogger( __name__ )


def download_pdf(pdf_url, title):
    """
    Download the PDF from the given URL and save it locally.

    :param pdf_url: The URL to download the PDF from.
    :param title: The title of the paper, used to name the PDF file.
    :return: The local path to the downloaded PDF, or None if download failed.
    """
    if not pdf_url:
        logger.warning( f"No PDF URL provided for paper: {title}" )
        return None

    try:
        response = requests.get( pdf_url, stream=True )
        if response.status_code == 200:
            # Clean the title to create a valid filename
            filename = f"{''.join( e for e in title if e.isalnum() or e in (' ', '_', '-') ).rstrip()}.pdf"
            pdf_dir = os.path.join( os.getcwd(), 'data', 'pdfs' )
            os.makedirs( pdf_dir, exist_ok=True )
            pdf_path = os.path.join( pdf_dir, filename )

            with open( pdf_path, 'wb' ) as f:
                for chunk in response.iter_content( chunk_size=8192 ):
                    if chunk:
                        f.write( chunk )

            logging.info( f"Downloaded PDF for paper: {title}" )
            return pdf_path
        else:
            logging.error( f"Failed to download PDF for paper: {title} - Status Code: {response.status_code}" )
            return None
    except Exception as e:
        logging.error( f"Exception occurred while downloading PDF for paper: {title} - {e}" )
        return None
