from flask import Blueprint, request, jsonify
from src.services.search_service import search_papers, search_citation

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': '需要关键词'}), 400

    results = search_papers(keyword)
    papers = [{'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results]
    return jsonify(papers)

@search_bp.route('/citations', methods=['GET'])
def citations():
    paper_id = request.args.get('paper_id', '')
    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400

    results = search_citation(paper_id)
    citations = [{'citing_paper_id': citation.citing_paper_id, 'cited_paper_id': citation.cited_paper_id} for citation in results]
    return jsonify(citations)