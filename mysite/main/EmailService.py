import smtplib, ssl
from email.message import EmailMessage
import logging
import configparser

'''
    Created by Osu Adefolarin on 22 January 2020
'''

# creating a custom logging config
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)

# Set the format of the logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# set the file to log in and the format to be logged
file_handler = logging.FileHandler('email_service.log')
file_handler.setFormatter(formatter)

# Adds the file handler to the logger
logger.addHandler(file_handler)

class EmailService:

    def __init__(self, email):
        self.email_model = email

        #Create a config_parser object
        try:
            logger.info("Creating configuration parser")
            self.config = configparser.ConfigParser()
            logger.info("Processing configurations...")
            self.config.read('application.properties')
            logger.info("Configuration gotten...")
        except configparser.ParsingError:
            logger.exception("Could not parse file, either file does not exist or is corrupted!!!")

        try:
            self.host = 'smtp.gmail.com'#self.config.get('server', 'smtp.client')
            self.email_address = 'folzieds@gmail.com' #self.config.get('property','email') # this is the auto sender
            self.password = 'jglyhyuekrxuapfv' #self.config.get('property','password')
        except configparser.NoSectionError:
            logger.exception("Could not find a property!!!")

        self.mail_content = f"{self.email_model.contact_email}:\n{self.email_model.contact_name}\n\n{self.email_model.email_body}"


    def mail_payload(self):
        mail = EmailMessage()
        mail['Subject'] = "MESSAGE FROM PORTFOLIO"
        mail['From'] = self.email_address
        mail['To'] = 'folzieds@gmail.com' #self.config.get('property','email_recepient')
        mail.set_content(self.mail_content)

        return mail

    def send_email(self):
        message = self.mail_payload()
        self.port = 587#self.config.get('server', 'host.port')

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()

                logger.info("About to login...")
                server.login(self.email_address, self.password)
                logger.info("login successful....")

                #send email here
                logger.info("sending message")
                server.send_message(message)
                logger.info("message sent...")
        except (smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused,smtplib.SMTPDataError,TimeoutError,ConnectionRefusedError):
            logger.exception("Could not send mail...")

    def send_email_ssl(self):
        message = self.mail_payload()
        self.port = 465 #self.config.get('server','host.port.ssl')

        try:
            with smtplib.SMTP_SSL(self.host,self.port) as smtp:

                logger.info("About to login...")
                smtp.login(self.email_address, self.password)
                logger.info("login successful....")
                smtp.send_message(message)

        except (smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused,smtplib.SMTPDataError,TimeoutError,ConnectionRefusedError):
            logger.exception("Could not send mail...")


