# src/example_fetch.py

from fetch_papers import fetch_papers

def main():
    query = "AI in VR mental health"
    papers = fetch_papers(query, limit=50)
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(author['name'] for author in paper['authors'])}")
        print(f"Year: {paper.get('year')}")
        print(f"DOI: {paper.get('doi')}\n")

if __name__ == "__main__":
    main()

