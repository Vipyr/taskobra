# Libraries
from sqlalchemy import Column, ForeignKey, Integer, Table
# Taskobra
from taskobra.orm.base import ORMBase


user_role_table = Table(
    "UserRole", ORMBase.metadata,
    Column("user_id", Integer, ForeignKey("User.unique_id")),
    Column("role_id", Integer, ForeignKey("Role.unique_id")),
)
