from flask import Blueprint, request, jsonify
from src.services.search_service import search_papers_by_name, search_paper_by_id,search_citation, search_similar, search_category

search_bp = Blueprint('search', __name__)

@search_bp.route('/search/name', methods=['GET'])
def search_by_name():
    # 必须参数
    keyword = request.args.get('keyword', '')
    # 非必须参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not keyword:
        return jsonify({'error': '需要关键词'}), 400

    results = search_papers_by_name(keyword, page, per_page)
    papers = [{'id':paper.id, 'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results['results']]
    return jsonify({
        'total_num': results['total_num'],
        'results': papers,
        'page': results['page'],
        'per_page': results['per_page']
    })

@search_bp.route('/search/id', methods=['GET'])
def search_by_id():
    paper_id = request.args.get('paper_id', '')
    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400

    result = search_paper_by_id(paper_id)
    if not result:
        return jsonify({'error': '找不到该paper'}), 404

    return jsonify({'id': result.id, 'title': result.title, 'abstract': result.abstract, 'category': result.category, 'year': result.year})

@search_bp.route('/search/citations', methods=['GET'])
def citations():
    paper_id = request.args.get('paper_id', '')
    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400

    results = search_citation(paper_id)
    citations = [{'id': paper.id, 'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results]
    return jsonify(citations)

@search_bp.route('/search/similar', methods=['GET'])
def similar():
    paper_id = request.args.get('paper_id', '', type=int)
    number = request.args.get('number', '', type=int)
    if not number:
        return jsonify({'error': 'invalid number of similar papers requested'}), 400
    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400


    results = search_similar(paper_id, int(number))
    papers = [{'id': paper.id,'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results]
    return jsonify(papers)

@search_bp.route('/search/category', methods=['GET'])
def category():
    # 必须参数
    paper_id = request.args.get('paper_id', '', type=int)
    # 非必须参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not paper_id:
        return jsonify({'error': '需要paper_id'}), 400

    results = search_category(paper_id, page, per_page)
    papers = [{'id': paper.id, 'title': paper.title, 'abstract': paper.abstract, 'category': paper.category, 'year': paper.year} for paper in results['results']]
    return jsonify({
        'total_num': results['total_num'],
        'results': papers,
        'page': results['page'],
        'per_page': results['per_page']
    })
