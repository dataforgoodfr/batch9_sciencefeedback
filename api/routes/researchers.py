from flask import current_app as app, jsonify, request

from repository.researchers import researchers_from


@app.route('/researchers')
def get_researchers():
    return jsonify(researchers_from(**request.args))
