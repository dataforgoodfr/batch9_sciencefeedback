import os
from flask_sqlalchemy import SQLAlchemy

from utils.config import APP_NAME, \
                         COMPOSITION
from utils.logger import logger

LOCALHOST_POSTGRES_URL = f'postgresql://{APP_NAME}_user:{APP_NAME}_password@apipostgresdb-{COMPOSITION}/{APP_NAME}_apipostgres'
POSTGRES_URL = os.environ.get('POSTGRES_URL', LOCALHOST_POSTGRES_URL)

db = SQLAlchemy(engine_options={ 'pool_size': 3 })


def delete():
    logger.info('Delete all the database...')
    for table in reversed(db.metadata.sorted_tables):
        print('Deleting table {}...'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    logger.info('Delete all the database...Done.')


def create():
    logger.info('Create all the database...')
    db.create_all()
    db.session.commit()
    logger.info('Create all the database...Done.')
