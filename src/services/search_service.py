from src.models import Paper, Citation, Feature, create_session
from sqlalchemy.orm import sessionmaker
from sklearn.neighbors import NearestNeighbors

# def search_papers(keyword):
#     session = create_session()
#     results = session.query(Paper).filter(Paper.title.contains(keyword)).all()
#     session.close()
#     return results
def search_papers_by_name(keyword, page=1, per_page=10):
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

def search_paper_by_id(paper_id):
    session = create_session()
    result = session.query(Paper).filter(Paper.id == paper_id).first()
    session.close()
    return result

def search_citation(paper_id):
    session = create_session()
    citation_ids = session.query(Citation).filter(Citation.citer_id == paper_id).all()
    results = [session.query(Paper).filter(Paper.id == citation.citee_id).first() for citation in citation_ids]
    session.close()
    return results

def feat2vec(feat):
    return [getattr(feat, f"feat{i}") for i in range(128)]

def search_similar(paper_id, number):
    session = create_session()
    feature = session.query(Feature).filter(Feature.paper_id == paper_id).all()
    feature_rows = session.query(Feature).all()
    features = [feat2vec(row) for row in feature_rows]
    nbs = NearestNeighbors(n_neighbors=number, algorithm='ball_tree').fit(features)
    distances, indices = nbs.kneighbors([feat2vec(feature[0])])

    # remove self
    similar = [int(index) for index in indices[0] if index != paper_id - 1]

    # results = [session.query(Paper).filter(Paper.id == index + 1).first() for index in similar]
    session.close()
    return similar

def search_category(paper_id, page=1, per_page=10):
    session = create_session()
    paper = session.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        session.close()
        return {'total_num': 0, 'results': [], 'page': page, 'per_page': per_page}

    query = session.query(Paper).filter(Paper.category == paper.category)
    total_num = query.count()
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    session.close()
    return {
        'total_num': total_num,
        'results': results,
        'page': page,
        'per_page': per_page
    }
