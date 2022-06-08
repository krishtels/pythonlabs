from lab3.celery import celery_app
from django.core.mail import send_mail

@celery_app.task
def send_notification(subject, message, user_sender_email, users_getting_email):
    send_mail(subject, message, user_sender_email, users_getting_email)
    return None