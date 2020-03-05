from ..ORMTestCase import ORMTestCase
from taskobra.orm import get_engine, get_session, ORMBase
from taskobra.orm import User, Role, System
from taskobra.orm import UserSystemRole


class TestUserSystemRole(ORMTestCase):
    def test_query_UserSystemRole(self):
        # Put some data into the db
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            user = User(name="Fred")
            system = System(name="Fred's Computer")
            administrator = Role(name="Administrator")
            reporter = Role(name="Reporter")
            observer = Role(name="Observer")
            UserSystemRole(user=user, system=system, role=administrator)
            UserSystemRole(user=user, system=system, role=reporter)
            UserSystemRole(user=user, system=system, role=observer)
            session.add(user)
        # Query the db and make sure everything lines up
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            users = session.query(User)
            systems = session.query(System)
            self.assertEqual(len(users[0].system_roles), 3)
            self.assertEqual(len(systems[0].user_roles), 3)
            for role in users[0].system_roles:
                self.assertIn(role, systems[0].user_roles)
                self.assertIs(role.user, users[0])
            for role in systems[0].user_roles:
                self.assertIn(role, users[0].system_roles)
                self.assertIs(role.system, systems[0])
            self.assertIn(systems[0], [role.system for role in users[0].system_roles])
            self.assertIn(users[0], [role.user for role in systems[0].user_roles])

    def test_UserSystemRole_user_property(self):
        user_system_role = UserSystemRole()
        user = User(name="Fred")
        user_system_role.user = user
        self.assertIn(user_system_role, user.system_roles)

    def test_UserSystemRole_system_property(self):
        user_system_role = UserSystemRole()
        system = System(name="Fred's Computer")
        user_system_role.system = system
        self.assertIn(user_system_role, system.user_roles)

    def test_UserSystemRole_creation(self):
        with self.subTest("No Arguments"):
            user_system_role = UserSystemRole()
            self.assertIsNone(user_system_role.user)
            self.assertIsNone(user_system_role.system)
            self.assertIsNone(user_system_role.role)
        with self.subTest("User Only"):
            user = User(name="Fred")
            user_system_role = UserSystemRole(user=user)
            self.assertIs(user_system_role.user, user)
            self.assertIsNone(user_system_role.system)
            self.assertIsNone(user_system_role.role)
        with self.subTest("System Only"):
            system = System(name="Fred's Computer")
            user_system_role = UserSystemRole(system=system)
            self.assertIsNone(user_system_role.user)
            self.assertIs(user_system_role.system, system)
            self.assertIsNone(user_system_role.role)
        with self.subTest("Role Only"):
            role = Role(name="Fred's Role")
            user_system_role = UserSystemRole(role=role)
            self.assertIsNone(user_system_role.user)
            self.assertIsNone(user_system_role.system)
            self.assertIs(user_system_role.role, role)
        with self.subTest("All"):
            user = User(name="Fred")
            system = System(name="Fred's Computer")
            role = Role(name="Fred's Role")
            user_system_role = UserSystemRole(user=user, system=system, role=role)
            self.assertIs(user_system_role.user, user)
            self.assertIs(user_system_role.system, system)
            self.assertIs(user_system_role.role, role)
