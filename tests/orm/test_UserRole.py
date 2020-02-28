from .ORMTestCase import ORMTestCase
from taskobra.orm import get_engine, get_session, ORMBase
from taskobra.orm import User, Role, System
from taskobra.orm import UserSystemRole


class TestUserSystemRole(ORMTestCase):
    def test_query_UserSystemRole(self):
        # Put some data into the db
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            user = User(name="Fred")
            administrator = Role(name="Administrator")
            reporter = Role(name="Reporter")
            observer = Role(name="Observer")
            user.roles.append(administrator)
            user.roles.append(reporter)
            user.roles.append(observer)
            session.add(user)
        # Query the db and make sure everything lines up
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            users = session.query(User)
            roles = session.query(Role)
            # Make sure there are 3 roles in the roles table
            self.assertEqual(len(list(roles)), 3)
            # Make sure there are 3 roles in the user's roles list
            self.assertEqual(len(users[0].roles), 3)
            # Make sure they're the same 3 roles
            for role in users[0].roles:
                self.assertIn(role, roles)
            for role in roles:
                self.assertIn(role, users[0].roles)
