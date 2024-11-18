# src/download_arxiv_papers.py

import os
import requests
import feedparser
from database_setup import session, Paper  # If used; else remove
import logging

# Configure logging
logging.basicConfig(
    filename='download_arxiv_papers.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def fetch_arxiv_papers(query, max_results=10):
    """
    Fetch papers from arXiv based on the query.
    """
    try:
        base_url = 'http://export.arxiv.org/api/query?'
        search_query = f'search_query=all:{query}'
        start = 0
        sortBy = 'relevance'
        sortOrder = 'descending'
        url = f"{base_url}{search_query}&start={start}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}"

        response = requests.get( url )
        if response.status_code != 200:
            logging.error( f"Error fetching papers from arXiv: {response.status_code}" )
            print( f"Error fetching papers from arXiv: {response.status_code}" )
            return []

        feed = feedparser.parse( response.text )
        papers = []
        for entry in feed.entries:
            # Extract DOI if available
            doi = None
            pdf_url = None
            for link in entry.get( 'links', [] ):
                if link.get( 'type' ) == 'application/pdf':
                    pdf_url = link.get( 'href' )
                elif link.get( 'rel' ) == 'alternate':
                    doi_link = link.get( 'href' )
                    if 'doi.org' in doi_link:
                        doi = doi_link.split( 'doi.org/' )[-1]

            paper = {
                'title': entry.title.replace( '\n', ' ' ).strip(),
                'authors': ', '.join( [author.name for author in entry.authors] ),
                'year': entry.published[:4],
                'abstract': entry.summary.replace( '\n', ' ' ).strip(),
                'doi': doi,
                'pdf_url': pdf_url if pdf_url else None
            }
            papers.append( paper )
        logging.info( f"Fetched {len( papers )} papers from arXiv." )
        return papers

    except Exception as e:
        logging.error( f"Exception in fetch_arxiv_papers: {e}" )
        print( f"Exception in fetch_arxiv_papers: {e}" )
        return []


def download_pdf(pdf_url, title, save_dir='../data/arxiv_pdfs'):
    """
    Download PDF from the given URL and save it to the specified directory.

    :param pdf_url: URL of the PDF to download.
    :param title: Title of the paper (used for naming the file).
    :param save_dir: Directory to save the downloaded PDF.
    :return: Local file path to the downloaded PDF or None if failed.
    """
    try:
        if not os.path.exists( save_dir ):
            os.makedirs( save_dir )
            logging.info( f"Created directory: {save_dir}" )
            print( f"Created directory: {save_dir}" )

        # Sanitize the title for filename
        filename = ''.join( c if c.isalnum() else '_' for c in title ) + '.pdf'
        filepath = os.path.join( save_dir, filename )

        # Check if the PDF already exists
        if os.path.exists( filepath ):
            logging.info( f"PDF already exists for: {title}" )
            print( f"PDF already exists for: {title}" )
            return filepath

        response = requests.get( pdf_url, stream=True )
        response.raise_for_status()

        with open( filepath, 'wb' ) as f:
            for chunk in response.iter_content( 1024 ):
                if chunk:
                    f.write( chunk )

        logging.info( f"Downloaded PDF for: {title}" )
        print( f"Downloaded PDF for: {title}" )
        return filepath

    except requests.exceptions.RequestException as e:
        logging.error( f"Failed to download PDF for {title}: {e}" )
        print( f"Failed to download PDF for {title}: {e}" )
        return None
