# src/store_papers.py

from database_setup import session, Paper
from download_papers import download_pdf
import logging

# Configure logging
logging.basicConfig( level=logging.DEBUG )
logger = logging.getLogger( __name__ )


def store_papers(papers):
    """
    Store fetched papers into the database and download their PDFs.
    Only processes papers that have an available PDF URL.

    :param papers: List of paper dictionaries fetched from APIs.
    """
    try:
        for p in papers:
            if not isinstance( p, dict ):
                logger.warning( f"Encountered non-dict paper: {p}" )
                continue

            # Extract DOI from externalIds
            external_ids = p.get( 'externalIds' ) or {}
            doi = external_ids.get( 'DOI' )

            # Extract PDF URL from openAccessPdf
            open_access_pdf = p.get( 'openAccessPdf' ) or {}
            pdf_url = open_access_pdf.get( 'url' )

            # **Skip papers without a PDF URL**
            if not pdf_url:
                logger.info( f"Skipping paper (no PDF available): {p.get( 'title', 'No Title' )}" )
                continue

            # Download PDF
            pdf_path = download_pdf( pdf_url, p['title'] ) if pdf_url else None

            # Avoid duplicates based on DOI or title
            if doi:
                exists = session.query( Paper ).filter_by( doi=doi ).first()
            else:
                exists = session.query( Paper ).filter_by( title=p['title'] ).first()

            if not exists:
                authors = ', '.join( [author['name'] for author in p.get( 'authors', [] )] )
                paper = Paper(
                    title=p['title'],
                    authors=authors,
                    year=int( p['year'] ) if p.get( 'year' ) and str( p['year'] ).isdigit() else None,
                    abstract=p.get( 'abstract', '' ),
                    citation_count=p.get( 'citationCount', 0 ),
                    doi=doi,
                    pdf_path=pdf_path  # Store the local PDF path
                )
                session.add( paper )
                logging.info( f"Added new paper to database: {paper.title}" )
            else:
                # Optionally, update the PDF path if not already set
                if not exists.pdf_path and pdf_path:
                    exists.pdf_path = pdf_path
                    logging.info( f"Updated PDF path for paper: {exists.title}" )
        session.commit()
        print( "Papers stored and PDFs downloaded successfully." )
        logging.info( "Papers stored and PDFs downloaded successfully." )
    except Exception as e:
        session.rollback()
        logging.error( f"An error occurred while storing papers: {e}" )
        print( f"An error occurred while storing papers: {e}" )
