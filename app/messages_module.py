import smtplib, ssl, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

sender_email = "devops.send@gmail.com"
password = os.getenv('password')


def send_email(receiver_email, subject, text):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
