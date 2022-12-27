from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import config

class Mailer:
    def __init__(self):
        self.server = SMTP_SSL(host='smtp.gmail.com', port=465)
        self.server.ehlo()
        self.server.login(config.EMAIL_ID, config.EMAIL_PASSWORD)
        self.email = config.EMAIL_ID
    
    def send_mail(self,filename = None, to = None, sub = None, body = None):
        if filename == None:
            filename = config.EXCEL_FILE_NAME
        if to == None:
            to = self.email
        if sub == None:
            sub = "TESTING"
        if body == None:
            body = "This is the test body"
        msg = MIMEMultipart()

        
        msg['From']=self.email
        msg['To']= to
        msg['Subject'] = sub
        msg.attach(MIMEText(body, 'plain'))
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
        msg.attach(part)
        mail_content = msg.as_string()
        self.server.sendmail(self.email, self.email, mail_content)









