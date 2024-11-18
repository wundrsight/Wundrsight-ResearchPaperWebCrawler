# src/app.py

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from database_setup import session, Paper
from dotenv import load_dotenv
from integrated_download import integrated_download
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use a secure key in production

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the search query from the form
        query = request.form.get('query')
        if not query:
            flash("Please enter a search query.", "error")
            return redirect(url_for('index'))

        try:
            # Perform the integrated download process with the query
            integrated_download(query, os.getenv('UNPAYWALL_EMAIL'), max_results=20)
            flash(f"Successfully fetched and processed papers for query: '{query}'", "success")
        except Exception as e:
            flash(f"An error occurred while fetching papers: {e}", "error")
            logger.error(f"Error in index route: {e}")

        # Redirect to the index to display updated papers
        return redirect(url_for('index'))

    # For GET requests, fetch all papers to display
    papers = session.query(Paper).all()
    return render_template('index.html', papers=papers)

@app.route('/download/<int:paper_id>')
def download_pdf(paper_id):  # Renamed from download_pdf_route to download_pdf
    paper = session.query(Paper).filter_by(id=paper_id).first()
    if not paper or not paper.pdf_path:
        flash("PDF not found.", "error")
        return redirect(url_for('index'))

    directory, filename = os.path.split(paper.pdf_path)
    if not os.path.exists(paper.pdf_path):
        flash("PDF file does not exist.", "error")
        return redirect(url_for('index'))

    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=3000, debug=True )
