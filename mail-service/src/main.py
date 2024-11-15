import asyncio
import time
import aiormq
import aiormq.abc
import aiohttp
import sys
import os

from src.models.mail_model import MailModel

def is_production():
    env = os.environ.get('ENVIRONMENT')

    return env is not None and env == 'production'

def get_api_key():
    api_key = os.environ.get('APIKEY')

    if api_key is None and len(sys.argv) > 2:
        api_key = sys.argv[2]

    return api_key

service_uid = "0"

if len(sys.argv) > 1:
    service_uid = sys.argv[1]

def send_mail(mail: MailModel):
    time.sleep(3)
    print(f'The mail {mail.uid} was succesfully sent!')

async def message_callback(message: aiormq.abc.DeliveredMessage):
    json_text = message.body.decode()
    mail = MailModel.model_validate_json(json_text)
    send_mail(mail)

    await message.channel.basic_ack(
        message.delivery.delivery_tag
    )
    api_key = get_api_key()
    if api_key is not None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{'web-api' if is_production() else 'localhost'}:8000/mail-services?service_uid={service_uid}&mail_uid={mail.uid}", headers={
                "Authorization": api_key
            }):
                pass

async def main():
    try_conection_counter = 1
    while True:
        if try_conection_counter > 100:
            break
        try:
            connection = await aiormq.connect(f"amqp://george:abcdef@{'service-bus' if is_production() else 'localhost'}:5672/")
            break
        except:
            time.sleep(1)
            try_conection_counter += 1


    channel = await connection.channel()
    await channel.basic_qos(prefetch_count=1)
    declare_ok = await channel.queue_declare(queue="mail_queue", durable=True)

    await channel.basic_consume(declare_ok.queue, message_callback)

loop = asyncio.get_event_loop()
loop.create_task(main())

loop.run_forever()
