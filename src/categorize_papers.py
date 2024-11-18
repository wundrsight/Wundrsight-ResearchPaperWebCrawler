# src/categorize_papers.py

from database_setup import session, Paper
import logging

# Configure logging
logging.basicConfig(
    filename='categorize_papers.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def categorize_papers(threshold=50):
    """
    Categorize papers based on citation counts.

    :param threshold: Citation count threshold to categorize as 'Core' or 'Supplementary'.
    """
    try:
        papers = session.query( Paper ).all()
        for paper in papers:
            if paper.citation_count >= threshold:
                paper.category = 'Core'
            else:
                paper.category = 'Supplementary'
            logging.info( f"Categorized paper '{paper.title}' as {paper.category}." )
        session.commit()
        print( "Papers categorized successfully." )
        logging.info( "Papers categorized successfully." )
    except Exception as e:
        session.rollback()
        logging.error( f"Exception in categorize_papers: {e}" )
        print( f"Exception in categorize_papers: {e}" )
