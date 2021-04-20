from redis import Redis
from rq import Queue
from rq.job import Job
from app.messages_module import send_email as smtp_send

queue = Queue('abc', connection=Redis())


def send_email(receiver, subject, text):
    message_args = {'receiver_email': receiver, 'subject': subject, 'text': text}
    job = Job.create(smtp_send, kwargs=message_args)
    queue.enqueue(job)  # os.fork не работает на винде(


send_email('buguev.nikita@gmail.com', 'abc', 'hahaha')
