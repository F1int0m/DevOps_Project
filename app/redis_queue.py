from redis import Redis
from rq import Queue
from app.messages_module import send_email

queue = Queue('abc', connection=Redis())

queue.enqueue(send_email) #os.fork не работает на винде(
