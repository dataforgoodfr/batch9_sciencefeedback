from flask import current_app as app, jsonify, request

from repository.keywords import keywords_from


@app.route('/keywords')
def get_keywords():
    return jsonify(keywords_from(**request.args))
