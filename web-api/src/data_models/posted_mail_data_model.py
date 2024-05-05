from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String

from src.data_models.base_data_model import BaseDataModel


class PostedMailDataModel(BaseDataModel):
    __tablename__ = "posted_mail"
    __table_args__ = {"schema": "business"}

    id: Mapped[int] = mapped_column(primary_key=True)
    mail_uid: Mapped[str] = mapped_column(String(256))
    date: Mapped[datetime] = mapped_column(DateTime())

    user_id: Mapped[int] = mapped_column(ForeignKey("admin.user.id"))

    user: Mapped["UserDataModel"] = relationship(back_populates="posted_mails")
