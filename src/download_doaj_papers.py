# src/download_doaj_papers.py

import os
import requests
import logging

# Configure logging
logging.basicConfig(
    filename='download_doaj_papers.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def search_doaj(query, page_size=10):
    """
    Search DOAJ for articles matching the query.

    :param query: Search query.
    :param page_size: Number of articles to fetch per page.
    :return: List of article dictionaries.
    """
    try:
        base_url = "https://doaj.org/api/v1/search/articles/"
        params = {
            'pageSize': page_size,
            'page': 1,
            'query': query
        }
        response = requests.get( base_url, params=params )
        if response.status_code == 200:
            results = response.json().get( 'results', [] )
            logging.info( f"Fetched {len( results )} articles from DOAJ." )
            return results
        else:
            logging.error( f"Error searching DOAJ: {response.status_code}" )
            print( f"Error searching DOAJ: {response.status_code}" )
            return []
    except Exception as e:
        logging.error( f"Exception in search_doaj: {e}" )
        print( f"Exception in search_doaj: {e}" )
        return []


def download_pdf(article, identifier, save_dir='../data/doaj_pdfs'):
    """
    Download PDF from DOAJ article metadata and save it to the specified directory.

    :param article: Dictionary containing article metadata.
    :param identifier: Unique identifier for the paper (e.g., title).
    :param save_dir: Directory to save the downloaded PDF.
    :return: Local file path to the downloaded PDF or None if failed.
    """
    try:
        links = article.get( 'bibjson', {} ).get( 'link', [] )
        pdf_links = [link['url'] for link in links if link.get( 'type' ) == 'fulltext']
        pdf_url = None
        for link in pdf_links:
            if link.endswith( '.pdf' ):
                pdf_url = link
                break

        if not pdf_url:
            logging.warning( f"No PDF link available for article: {identifier}" )
            print( f"No PDF link available for article: {identifier}" )
            return None

        if not os.path.exists( save_dir ):
            os.makedirs( save_dir )
            logging.info( f"Created directory: {save_dir}" )
            print( f"Created directory: {save_dir}" )

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
