from flask import current_app as app, jsonify, request

from repository.keywords import keywords_from


@app.route('/keywords')
def get_keywords():
    search_query = request.args.get('search_query')
    min_score = int(request.args.get('min_score'))
    if not search_query or not min_score:
        return jsonify([])
    return jsonify(keywords_from(search_query=search_query, min_score=min_score))
