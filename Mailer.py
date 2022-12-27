from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import config

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage


class Mailer:
    def __init__(self):
        try:
            self.server = SMTP_SSL(host='smtp.gmail.com', port=465)
            self.server.ehlo()
            self.server.login(config.EMAIL_ID, config.EMAIL_PASSWORD)
        except:
            pass
        self.email = config.EMAIL_ID

    def send_gmail(self, attachments: list = None, subject: str = "TESTING", messageBody: str = ""):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        try:
            service = build('gmail', 'v1', credentials=creds)
            message = EmailMessage()
            message.set_content(messageBody)
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as content_file:
                        content = content_file.read()
                        message.add_attachment(content, maintype='application', subtype=(
                            attachment.split('.')[1]), filename=attachment)

            message['To'] = config.EMAIL_ID
            message['From'] = 'paulnikhil123@gmail.com'
            message['Subject'] = subject

            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }

            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
            print(send_message)
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        return send_message
