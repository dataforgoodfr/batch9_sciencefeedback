from sqlalchemy import BigInteger, \
                       Column, \
                       String
from utils.database import db


class Researcher(db.Model):

    email = Column(String(120),
                   nullable=False,
                   unique=True)

    firtName = Column(String(128))

    lastName = Column(String(128))

    id = Column(BigInteger(),
                primary_key=True,
                autoincrement=True)
