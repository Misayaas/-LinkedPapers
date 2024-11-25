from flask import Blueprint, request, jsonify
from src.services.search_service import search_papers, search_citation, search_similar

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': '需要关键词'}), 400

    results = search_papers(keyword)
    papers = [{'id':paper.id, 'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results]
    return jsonify(papers)

@search_bp.route('/citations', methods=['GET'])
def citations():
    paper_id = request.args.get('paper_id', '')
    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400

    results = search_citation(paper_id)
    citations = [{'citer_id': citation.citer_id, 'citee_id': citation.citee_id} for citation in results]
    return jsonify(citations)

@search_bp.route('/similar', methods=['GET'])
def search_similar():
    paper_id = request.args.get('paper_id', '')
    number = request.args.get('number', '')
    if not number:
        return jsonify({'error': 'invalid number of similar papers requested'}), 400
    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400


    results = search_similar(paper_id, number)
    papers = [{'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results]
    return jsonify(papers)
