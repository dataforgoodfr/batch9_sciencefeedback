from flask import current_app as app, jsonify, request

from repository.researchers import researchers_from


@app.route('/researchers')
def get_researchers():
    k = int(request.args.get('k'))
    keywords = request.args.get('keywords')
    if not k or not keywords:
        return jsonify([])
    return jsonify(researchers_from(k=k, keywords=keywords))
