from src.models import Paper, Citation, create_session
from sqlalchemy.orm import sessionmaker

def search_papers(keyword):
    session = create_session()
    results = session.query(Paper).filter(Paper.title.contains(keyword)).all()
    session.close()
    return results

def search_citation(paper_id):
    session = create_session()
    results = session.query(Citation).filter(Citation.paper_id == paper_id).all()
    session.close()
    return results