# src/database_setup.py

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Paper

# Configure logging
logging.basicConfig(
    filename='database_setup.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def setup_database():
    """
    Sets up the database by creating the necessary tables and returning a session.
    """
    try:
        # Get the absolute path to the 'data' directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(current_dir, '..', 'data'))

        # Ensure the 'data' directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"Created directory: {data_dir}")
            print(f"Created directory: {data_dir}")

        # Define the database path
        db_path = os.path.join(data_dir, 'literature.db')

        # Create the SQLite engine using the absolute path
        engine = create_engine(f'sqlite:///{db_path}', echo=False)

        # Create all tables in the database
        Base.metadata.create_all(engine)
        logging.info("Database setup complete.")
        print("Database setup complete.")

        # Create a configured "Session" class
        Session = sessionmaker(bind=engine)

        # Create a Session instance
        session = Session()
        logging.info("Session created successfully.")
        print("Session created successfully.")

        return session

    except Exception as e:
        logging.error(f"An error occurred while setting up the database: {e}")
        print(f"An error occurred while setting up the database: {e}")
        return None

# Initialize the database and create a session when the module is imported
session = setup_database()
