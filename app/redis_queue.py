from rq.job import Job
from app.messages_module import send_email as smtp_send
from redis import Redis
from rq import Queue

redis = Redis()
q = Queue(connection=redis)


def send_email(receiver, subject, text):
    message_args = {'receiver_email': receiver, 'subject': subject, 'text': text}
    job = Job.create(smtp_send, kwargs=message_args, connection=redis)
    q.enqueue_job(job)  # os.fork не работает на винде(


send_email('buguev.nikita@gmail.com', 'abc', 'hahaha')
