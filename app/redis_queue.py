import datetime
from redis import Redis
from rq import Queue
from rq.job import Job
from app.messages_module import send_email as smtp_send
from .order import check_order

redis = Redis()
q = Queue(connection=redis)


def send_email(receiver, subject, text):
    message_args = {'receiver_email': receiver, 'subject': subject, 'text': text}
    job = Job.create(smtp_send, kwargs=message_args, connection=redis)
    q.enqueue_job(job)  # os.fork не работает на винде(


def remind_old_order(user_id, old_cart):
    kwargs = {'user_id': user_id, 'cart': old_cart}
    c = q.enqueue_in(datetime.timedelta(seconds=5), check_order, kwargs=kwargs)
    print(c)
