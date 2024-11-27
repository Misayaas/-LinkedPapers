from src.models import Paper, Citation, Feature, create_session
from sqlalchemy.orm import sessionmaker
from sklearn.neighbors import NearestNeighbors

# def search_papers(keyword):
#     session = create_session()
#     results = session.query(Paper).filter(Paper.title.contains(keyword)).all()
#     session.close()
#     return results
def search_papers(keyword, page=1, per_page=10):
    session = create_session()
    query = session.query(Paper).filter(Paper.title.contains(keyword))
    total_num = query.count()
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    session.close()
    return {
        'total_num': total_num,
        'results': results,
        'page': page,
        'per_page': per_page
    }

def search_citation(paper_id):
    session = create_session()
    citation_ids = session.query(Citation).filter(Citation.citer_id == paper_id).all()
    results = [session.query(Paper).filter(Paper.id == citation.citee_id).first() for citation in citation_ids]
    session.close()
    return results

def search_similar(paper_id, number):
    session = create_session()
    feature = session.query(Feature).filter(Feature.paper_id == paper_id).all()
    nbs = NearestNeighbors(n_neighbors=number, algorithm='ball_tree').fit(session.query(Feature).all())
    distances, indices = nbs.kneighbors(feature)

    results = [session.query(Paper).filter(Paper.id == index).first() for index in indices]
    session.close()
    return results
