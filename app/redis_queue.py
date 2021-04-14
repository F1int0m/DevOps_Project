from redis import Redis
from rq import Queue
from messages_module import Send_email

queue = Queue('abc', connection=Redis())

#queue.enqueue(Send_email, 'content') #os.fork не работает на винде(
