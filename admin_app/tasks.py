from toy_shop.celery import app
from .service import send


@app.task
def send_for_users_phone(phones):
    send(phones)

