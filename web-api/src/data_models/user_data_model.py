from typing import List
from src.data_models.base_data_model import BaseDataModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class UserDataModel(BaseDataModel):
    __tablename__ = "user"
    __table_args__ = {"schema": "admin"}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(128))
    posted_mails: Mapped[List["PostedMailDataModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
