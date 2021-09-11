# flake8: noqa: E501
import smtplib

from loguru import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader


class SendMail:
    def __init__(self, username, password, port, smtp_server):
        self.username = username
        self.password = password
        self.port = port
        self.smtp_server = smtp_server

    def send_mail(self, receiver_email, subject):
        msg = MIMEMultipart("alternative")
        msg["From"] = self.username
        msg["To"] = receiver_email
        msg["Subject"] = subject
        # TODO: Add template
        # templates_env = Environment(loader=FileSystemLoader(searchpath="service1/templates"))
        # template = templates_env.get_template('email.html')
        # html = template.render(button_href=button_href, button_text=button_text,
        #                        sent_message=sent_message, user_name=user_name)

        mime_text = MIMEText("Lorem ip.", "html")
        msg.attach(mime_text)

        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.port)
            server.login(self.username, self.password)
            server.sendmail(self.username, receiver_email, msg.as_string())
            server.quit()
            logger.info(f"Mail sent to {receiver_email}")
        except Exception as e:
            logger.error(f"Mail not sent to {receiver_email}")
            logger.error(e)
