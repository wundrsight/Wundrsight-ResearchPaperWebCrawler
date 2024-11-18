# src/automated_workflow.py

import schedule
import time
from integrated_download import integrated_download
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def job():
    print("Starting automated literature review job...")
    query = "AI in VR mental health"
    email = os.getenv('UNPAYWALL_EMAIL')
    if not email:
        print("UNPAYWALL_EMAIL not set in environment variables.")
        return
    integrated_download(query, email, max_results=3)
    print("Automated job completed.")

# Schedule the job to run every Monday at 09:00 AM
schedule.every().monday.at("09:00").do(job)

print("Scheduler started. Waiting for scheduled jobs...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
