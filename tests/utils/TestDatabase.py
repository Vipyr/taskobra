import os 
from sqlalchemy.orm import sessionmaker
from taskobra.orm import get_engine, ORMBase


class TestDatabase(object):
    def __init__(self, database_uri, data_generator):
        # Initialize the databse 
        self.database_uri = database_uri
        self.data_generator = data_generator
        self.engine = get_engine(self.database_uri)
        self.session = sessionmaker(bind=self.engine)()
        ORMBase.metadata.create_all(self.session.bind)

    def __enter__(self):
        # Generate and commit the test data 
        for db_object in self.data_generator():
            self.session.add(db_object)
        self.session.commit()

        # Handle ENV Vars for the Web Application
        self.env_database_uri = os.environ.get('DATABASE_URI', '')
        os.environ['DATABASE_URI'] = self.database_uri
        return self.session

    def __exit__(self, type, value, traceback):
        if type is None:
            self.session.commit()
            self.session.close()
        else:
            self.session.rollback()
            self.session.close()
        return True

