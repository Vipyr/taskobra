from unittest import TestCase
from taskobra.orm import get_engine, get_session, ORMBase


class ORMTestCase(TestCase):
    def tearDown(self):
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            for table in session.execute("SELECT * FROM sqlite_master WHERE type='table'"):
                session.execute(f"DELETE FROM '{table[1]}'")
