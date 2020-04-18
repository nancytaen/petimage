import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import Config


def send_mail(to_addr, subject, text=None, html=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = Config.SMTP_MAIL_ADDR
    msg["To"] = to_addr
    msg["Subject"] = subject

    if text:
        msg.attach(MIMEText(text, "plain"))
    if html:
        msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(Config.SMTP_MAIL_ADDR, Config.SMTP_MAIL_PWD)
        server.sendmail(Config.SMTP_MAIL_ADDR, to_addr, msg.as_string())
    except Exception as e:
        print(e)
        print("Something went wrong")
        return False
