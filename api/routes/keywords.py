from flask import current_app as app, jsonify
import utils.nlp

MOCK_KEYWORDS = [
	'thrombosis',
	'vaccine',
	]


@app.route('/keywords')
def get_keywords():
    return jsonify(MOCK_KEYWORDS)
