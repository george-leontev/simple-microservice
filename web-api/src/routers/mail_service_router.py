import uuid

from fastapi.routing import APIRouter
from fastapi.responses import Response

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
async def get_acknowledgement(mail_uid: str):
    print(f"Email was sent with the uid: {mail_uid}")
    await sio.emit("get_acknowledgement", data=mail_uid)

    return Response(status_code=200)
