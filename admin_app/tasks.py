from toy_shop.celery import app
from .service import send


@app.task
def send_for_users_phone(phone_list, stock):
    print('ok')
    send(phone_list, stock)

@app.task
def add(x, y):
    return x / y
