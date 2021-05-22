import os, sys, dotenv

from redis import Redis
from rq import Worker, Connection, Queue

dotenv.load_dotenv()
listen = ['default']
conn = Redis(host=os.getenv('redis_server'), port=os.getenv('redis_port'))

if __name__ == '__main__':
    with Connection(conn):
        w = Worker(list(map(Queue, listen)))
        w.work()
