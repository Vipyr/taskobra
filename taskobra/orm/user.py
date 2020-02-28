# Libraries
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# Taskobra
from taskobra.orm.base import ORMBase
from taskobra.orm.associations import user_role_table


class User(ORMBase):
    __tablename__ = "User"
    unique_id = Column(Integer, primary_key=True)
    name = Column(String)
    roles = relationship("Role", secondary=user_role_table)
    system_roles = relationship("UserSystemRole")

    def __repr__(self):
        return f"<User(name={self.name}, {self.roles}, {self.system_roles}, unique_id={self.unique_id})>"
