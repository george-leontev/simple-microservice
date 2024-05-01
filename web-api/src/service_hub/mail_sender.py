import aiormq

from src.models.mail_model import MailModel


async def send_mail_request(mail: MailModel):
    connection = await aiormq.connect('amqp://george:abcdef@localhost:5672/')

    channel = await connection.channel()

    channel.queue_declare(queue="mail_queue", durable=True)

    body = mail.model_dump_json()
    await channel.basic_publish(
        exchange="",
        routing_key="mail_queue",
        body=body.encode()
    )

    await connection.close()
