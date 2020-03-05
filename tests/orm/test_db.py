from .ORMTestCase import ORMTestCase
from sqlalchemy import create_engine
from taskobra.orm.base import get_session, get_sessionmaker


class TestDatabase(ORMTestCase):
    def test_get_session(self):
        engine = create_engine("sqlite:///:memory:")
        with get_session(bind=engine) as session:
            self.assertIs(session.bind, engine)

    def test_get_sessionmaker(self):
        engine = create_engine("sqlite:///:memory:")
        s1 = get_sessionmaker(bind=engine)
        s2 = get_sessionmaker(bind=engine)
        self.assertIs(s1, s2)
