from flask import current_app as app, jsonify


MOCK_SCIENTISTS = [
    { 'firstName': 'Michel', 'lastName': 'Guillemin' },
    { 'firstName': 'Clara', 'lastName': 'Debreuille' }
]


@app.route('/researchers')
def get_researchers():
    return jsonify(MOCK_SCIENTISTS)
