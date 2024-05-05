import uuid

from datetime import datetime, UTC

from fastapi.routing import APIRouter
from fastapi.responses import Response

from src.data_models.posted_mail_data_model import PostedMailDataModel
from src.data_access.data_access import SessionLocal
from src.service_hub.mail_sender import send_mail_request
from src.models.mail_model import MailModel
from src.web_socket_hub import sio


router = APIRouter(prefix="/mail-services", tags=["Services"])


@router.post("")
async def send_mail(mail: MailModel):
    mail.uid = uuid.uuid4().hex
    await send_mail_request(mail)
    print(f"Email was set into a queue with the uid: {mail.uid}")

    return Response(status_code=200)


@router.get("")
async def get_acknowledgement(service_uid: str, mail_uid: str):
    with SessionLocal() as session:
        session.add(
            PostedMailDataModel(
                mail_uid=mail_uid,
                date=datetime.now(UTC),
                user_id=1
            )
        )
        session.commit()
        
    await sio.emit(
        "get_acknowledgement", data={"service_uid": service_uid, "mail_uid": mail_uid}
    )

    return Response(status_code=200)
