from src.models import Paper, Citation, Feature, create_session
from sqlalchemy.orm import sessionmaker
from sklearn.neighbors import NearestNeighbors
from pymilvus import MilvusClient
import time
import json

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

    results = [session.query(Paper).filter(Paper.id == index + 1).first() for index in similar]
    session.close()
    return results

def search_similar_fast(paper_id, number):

    session = create_session()
    client = MilvusClient("feat.db")

    client.load_collection("feat")

    query_vector = client.query("feat", ids=[paper_id], output_fields=["vector"])[0]['vector']

    res = client.search(
        collection_name="feat",  # target collection
        data=[query_vector],  # query vectors
        limit=number,  # number of returned entities
        output_fields=["id"],  # specifies fields to be returned
        search_params={
            "metric_type": "IP",
            "params": {}
        }
    )

    ids = [row['id'] for row in res[0] if row['id'] != paper_id]
    results = [session.query(Paper).filter(Paper.id == index).first() for index in ids]
    return results


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
