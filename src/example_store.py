# src/example_store.py

from fetch_papers import fetch_papers
from store_papers import store_papers

def main():
    query = "AI in VR mental health"
    papers = fetch_papers(query, limit=50)
    store_papers(papers)

if __name__ == "__main__":
    main()
