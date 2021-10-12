from celery import Celery

app = Celery()

broker_url = 'amqp://localhost'

timezone = 'Europe/Oslo'

enable_utc = True
