# src/models.py

# src/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class Paper( Base ):
    __tablename__ = 'papers'

    id = Column( Integer, primary_key=True )
    title = Column( String, nullable=False )
    authors = Column( String, nullable=True )
    year = Column( Integer, nullable=True )
    abstract = Column( Text, nullable=True )
    citation_count = Column( Integer, default=0 )
    doi = Column( String, unique=True, nullable=True )
    pdf_path = Column( String, nullable=True )
    category = Column( String, nullable=True )  # e.g., Core, Supplementary

    def __repr__(self):
        return f"<Paper(title='{self.title}', authors='{self.authors}', year={self.year})>"
