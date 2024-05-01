import asyncio
import time
import aiormq
import aiormq.abc
import aiohttp

from src.models.mail_model import MailModel

def send_mail(mail: MailModel):
    print(mail.message)
    time.sleep(10)
    print('The mail was succesfully sent!')

async def message_callback(message: aiormq.abc.DeliveredMessage):

    json_text = message.body.decode()
    mail = MailModel.model_validate_json(json_text)
    send_mail(mail)

    await message.channel.basic_ack(
        message.delivery.delivery_tag
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8000/mail-services?mail_uid={mail.uid}"):
            pass

async def main():
    connection = await aiormq.connect('amqp://george:abcdef@localhost:5672/')

    channel = await connection.channel()
    await channel.basic_qos(prefetch_count=1)
    declare_ok = await channel.queue_declare(queue="mail_queue", durable=True)


    await channel.basic_consume(declare_ok.queue, message_callback)

loop = asyncio.get_event_loop()
loop.create_task(main())

loop.run_forever()
