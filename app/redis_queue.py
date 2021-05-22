from rq.job import Job
from app.messages_module import send_email as smtp_send
import requests
from . import q
from app.worker import conn



def send_email(receiver, subject, text):
    message_args = {'receiver_email': receiver, 'subject': subject, 'text': text}
    job = Job.create(smtp_send, kwargs=message_args, connection=conn)
    q.enqueue_job(job)  # os.fork не работает на винде(


def remind_old_order(user_id, old_cart):
    payload = {
        "method": 'get_cart',
        "params": {'user_id': user_id},
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post('http://127.0.0.1:8000' + '/api/v1/jsonrpc', json=payload)
    print(response)


send_email('nikita.buguev@gmail.com', '123321', '321')
