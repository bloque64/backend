__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
import os


blq_admin_user = os.environ["BLQ_ADMIN_USER"]
blq_admin_password = os.environ["BLQ_ADMIN_PASSWORD"]
blq_db_host = os.environ["BLQ_DB_HOST"]
blq_db_name = os.environ["BLQ_DB_NAME"]

connection_string = "mysql+pymysql://%s:%s@%s/%s" % (blq_admin_user, blq_admin_password, blq_db_host, blq_db_name)
#connection_string = "mysql://%s:%s@%s/%s" % (sscbot_admin_user, sccbot_admin_password, sccbot_db_host, sccbot_db_name)

session_instance = None

base = declarative_base()

class User(base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_member_name = Column(String(50))
    discord_member_id = Column(String(50))
    steem_account = Column(String(30))
    role = Column(String(10))          # "CURATOR", "CLEANER"
    level = Column(String(10))         # "BEGNNER, GOOD, EXCELENT, MASTER
    verification_status = Column(String(10))   # "PENDING", "ACCEPTED", "REJECTED"
    verification_token = Column(String(100))
    reputation = Column(Integer)               # Integer 0 to 100
    registerd_on = Column(DateTime)
    validated_on = Column(DateTime)
    is_admin = Column(Boolean)



    def to_json(self):

        return(self.steem_account)
    
    def __repr__(self):
        return "<User(discord_name='%s' (%s), steem_name='%s')>" % (self.discord_member_name, self.discord_member_id, self.steem_account)
    
    def __init__(self, discord_member_name = None, discord_member_id = None, steem_account=None):

        self.discord_member_name = discord_member_name
        self.discord_member_id = discord_member_id
        self.steem_account = steem_account

    

class Post(base):

    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    permalink = Column(String(256))
    fulllink = Column(String(256))
    link_poster = Column(String(256))
    author = Column(String(30))
    category = Column(String(50))
    upvotes = Column(Integer)
    #promoted_by = Column(User)

class Category(base):

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    description = Column(String(256))


class BlackListedUser(base):

    __tablename__ = 'black_list'
    id = Column(Integer, primary_key=True)
    steem_account = Column(String(30))
    reason = Column(String(256))

def return_session():

    engine = create_engine(connection_string, echo=False)
    Session = sessionmaker(bind=engine)
    session_instance = Session()
    return(session_instance)

def drop_tables():

    engine = create_engine(connection_string, echo=False)
    base.metadata.bind = engine
    base.metadata.drop_all()


def create_tables():

    engine = create_engine(connection_string, echo=False)
    base.metadata.create_all(engine)

def get_users():
    return(session_instance.query(User))


def reset_and_inicialize():
    drop_tables()
    create_tables()
    populate_default_categories()


def populate_default_categories():
    exit

if __name__ == "__main__":

    reset_and_inicialize()
