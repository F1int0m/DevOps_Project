import os, sys

from redis import Redis
from rq import Worker, Connection

listen = ['default']

conn = Redis(host=os.getenv('redis_server'), port=6379)

if __name__ == '__main__':
    with Connection(conn):
        qs = sys.argv[1:] or ['default']
        w = Worker(qs)
        w.work()
