# Libraries
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# Taskobra
from taskobra.orm.base import ORMBase
from taskobra.orm.associations import user_role_table


class System(ORMBase):
    __tablename__ = "System"
    unique_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_roles = relationship("UserSystemRole")

    def __repr__(self):
        return f"<System(name={self.name}, {self.user_roles}, unique_id={self.unique_id})>"
