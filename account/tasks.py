
from muscles_service.celery import app
from .service import mail


@app.task
def send_greetings_email(email):
    mail(email)

