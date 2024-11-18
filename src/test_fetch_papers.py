# src/test_fetch_papers.py

from fetch_papers import fetch_papers


def test_fetch_papers():
    query = "AI in VR therapy"
    limit = 5
    papers = fetch_papers( query, limit )
    if papers:
        print( f"Fetched {len( papers )} papers:" )
        for paper in papers:
            # Safely extract DOI
            doi = paper.get( 'externalIds', {} ).get( 'DOI', 'N/A' )

            # Safely extract PDF URL
            open_access_pdf = paper.get( 'openAccessPdf' ) or {}
            pdf_url = open_access_pdf.get( 'url', 'N/A' )

            print( f"Title: {paper.get( 'title', 'No Title' )}" )
            print( f"DOI: {doi}" )
            print( f"PDF URL: {pdf_url}\n" )
    else:
        print( "No papers fetched." )


if __name__ == "__main__":
    test_fetch_papers()
