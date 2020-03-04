# Libraries
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
# Taskobra
from taskobra.orm.base import ORMBase


class UserSystemRole(ORMBase):
    __tablename__ = "UserSystemRole"
    user_id = Column(Integer, ForeignKey("User.unique_id"), primary_key=True)
    system_id = Column(Integer, ForeignKey("System.unique_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("Role.unique_id"), primary_key=True)

    _user = relationship("User")
    _system = relationship("System")
    role = relationship("Role")

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user: "takobra.orm.User"):
        # Clean up and delete our current User reference
        del self.user
        # Update our reference to the new one
        self._user = user
        self._user.system_roles.append(self)

    @user.deleter
    def user(self):
        if self._user:
            self._user.system_roles.remove(self)
            del self._user

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system: "takobra.orm.System"):
        # Clean up and delete our current System reference
        del self.system
        # Update our reference to the new one
        self._system = system
        self._system.user_roles.append(self)

    @system.deleter
    def system(self):
        if self._system:
            self._system.user_roles.remove(self)
            del self._system

    def __repr__(self):
        return f"<UserSystemRole({self.user.name}, {self.system.name}, {self.role.name})>"
