from unittest import TestCase
from taskobra.orm import init_db
from taskobra.orm.base import Session, ORMBase
from taskobra.orm import User, Role, System
from taskobra.orm import UserSystemRole


class TestUser(TestCase):
    def test_table(self):
        init_db("sqlite:///:memory:")#, echo=True)
        session = Session()

        user = User(name="Fred")
        role = Role(name="Administrator")
        system = System(name="Fred's Computer")

        user.roles.append(role)

        UserSystemRole(user=user, system=system, role=role)

        session.add(user)

        print(user)
        print(system)
        print(role)

        user_q = session.query(User).first()

        print(user is user_q)

        self.assertTrue(user is session.query(User).first())
        self.assertEqual(user.name, session.query(User).first().name)
        user_q.name = "Frank"
        self.assertEqual(user.name, session.query(User).first().name)
        print(user_q)

        print()
        print(user)
        print(system)
        print(role)
