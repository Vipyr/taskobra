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
            system = System(name="Fred's Computer")
            UserSystemRole(user=user, system=system, role=administrator)
            UserSystemRole(user=user, system=system, role=reporter)
            UserSystemRole(user=user, system=system, role=observer)
            session.add(user)
        # Query the db and make sure everything lines up
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            users = session.query(User)
            systems = session.query(System)
            # self.assertEqual(len(users[0].system_roles), 3)
            for role in users[0].system_roles:
                self.assertIn(role, systems[0].user_roles)
                self.assertIs(role.user, users[0])
            for role in systems[0].user_roles:
                self.assertIn(role, users[0].system_roles)
                self.assertIs(role.system, systems[0])

    # def test_table(self):
    #     with get_session(bind=get_engine("sqlite:///:memory:")) as session:
    #         user = User(name="Fred")
    #         role = Role(name="Administrator")
    #         system = System(name="Fred's Computer")
    #         user.roles.append(role)
    #         UserSystemRole(user=user, system=system, role=role)
    #         session.add(user)

    #         print(user)
    #         print(system)
    #         print(role)

    #         user_q = session.query(User)[-1]

    #         print(user is user_q)

    #         self.assertTrue(user is session.query(User)[-1])
    #         self.assertEqual(user.name, session.query(User)[-1].name)
    #         user_q.name = "Frank"
    #         self.assertEqual(user.name, session.query(User)[-1].name)
    #         print(user_q)

    #         print()
    #         print(user)
    #         print(system)
    #         print(role)
