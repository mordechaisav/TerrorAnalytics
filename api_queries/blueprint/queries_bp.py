from flask import Blueprint, request, jsonify

from api_queries.queries1_repo import get_top_attack_types, group_with_most_casualties

queries_bp = Blueprint('queries', __name__)


@queries_bp.route('top_attack_types',methods=['GET'])
def top_attack_types():
    #pull arguments limit
    limit = request.args.get('limit')
    if limit:
        limit = int(limit)
        results = get_top_attack_types(limit)
    else:
        results = get_top_attack_types()
    if results:
        return jsonify({'attack_types':results}), 200

    return jsonify({'error': 'No attack types found'}), 404
#most_casualties
@queries_bp.route('most_casualties', methods=['GET'])
def most_casualties():

    results = group_with_most_casualties()
    if results:
        return jsonify({'casualties': results}), 200

    return jsonify({'error': 'No casualties found'}), 404
