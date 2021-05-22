import os, sys

from redis import Redis
from rq import Worker, Connection, Queue

listen = ['default']

conn = Redis(host=os.getenv('redis_server'), port=6379)

if __name__ == '__main__':
    with Connection(conn):
        w = Worker(list(map(Queue, listen)))
        w.work()
