# pylint: disable=C0415
# pylint: disable=R0913
# pylint: disable=R0914
# pylint: disable=R1719
# pylint: disable=W0611
# pylint: disable=W0612
# pylint: disable=W0613
import os

from flask_cors import CORS
from models import import_models
from routes import import_routes
from utils.config import IS_APP, \
                         IS_DEVELOPMENT, \
                         WEBAPP_URL
from utils.database import db, POSTGRES_URL
from utils.nltk import import_nltk


def setup(flask_app,
          with_cors=True,
          with_debug=False,
          with_routes=False,
          with_track_modifications=False):

    flask_app.secret_key = os.environ.get('FLASK_SECRET', '+%+5Q83!abR+-Dp@')

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = with_track_modifications

    if with_debug:
        flask_app.config['DEBUG'] = True

    db.app = flask_app
    db.init_app(flask_app)

    flask_app.url_map.strict_slashes = False

    @flask_app.teardown_request
    def remove_db_session(exc):
        try:
            db.session.remove()
        except AttributeError:
            pass

    if with_cors:
        cors = CORS(flask_app,
                    resources={r"/*": {"origins": WEBAPP_URL}},
                    supports_credentials=True)

    flask_app.app_context().push()
    import_models()
    import_nltk()

    if with_routes:
        import_routes()
