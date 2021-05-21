from flask import current_app as app, jsonify

from repository.checks import check_from_model
from utils.database import db


@app.route('/checks/<name>', methods=['GET'])
def get_check(name):
    model = None
    for v in db.Model._decl_class_registry.values():
        if hasattr(v, '__table__') and name.title() == v.__name__:
            model = v
    database_working, output = check_from_model(model)
    return_code = 200 if database_working else 500
    return jsonify(output), return_code
