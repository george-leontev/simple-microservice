import uuid

from datetime import datetime, UTC


from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import Response

from src.data_models.posted_mail_data_model import PostedMailDataModel
from src.data_access.data_access import SessionLocal
from src.service_hub.mail_sender import send_mail_request
from src.models.mail_model import MailModel
from src.web_socket_hub import sio
from src.utils.auth_helper import authorize


router = APIRouter(prefix="/mail-services", tags=["Services"])


@router.post("")
@authorize
async def send_mail(mail: MailModel, request: Request):
    mail.uid = uuid.uuid4().hex
    await send_mail_request(mail)

    return Response(status_code=200)

@router.get("")
@authorize
async def get_acknowledgement(service_uid: str, mail_uid: str, request: Request):
    with SessionLocal() as session:
        session.add(
            PostedMailDataModel(mail_uid=mail_uid, date=datetime.now(UTC), user_id=1)
        )
        session.commit()

    await sio.emit(
        "get_acknowledgement", data={"service_uid": service_uid, "mail_uid": mail_uid}
    )

    return Response(status_code=200)
