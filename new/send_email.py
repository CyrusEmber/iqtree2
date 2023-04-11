import logging
import smtplib, ssl
import os
from email.mime.text import MIMEText
import argparse

from logger import gen_log

logger = gen_log("test")
# Parse command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--to', dest='to_email', help='the email receiver')
parser.add_argument('-s', '--sub', dest='subject', help='email subject')


# Parse the command-line arguments
args = parser.parse_args()

# the email address to send the email
server = 'smtp.gmail.com'
port = 587
username = 'cyrusiris1@gmail.com'
password = 'Daohaomei77'

# Email settings
to_email = ''
from_email = username
email_subject = ''
email_body = ''

# Access the options
if args.to_email:
    logger.info(f'Send email to: {args.to_email}')
    to_email = args.to_email
else:
    logger.error("No email specified")

if not args.subject:
    logger.error("No subject specified")

# Access the log file and concatenate it to the email body
# find log file that is in the same directory as this script
for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    if file.endswith(".log"):
        print(file)





# Create the email message
msg = MIMEText(email_body)
msg['Subject'] = email_subject
msg['From'] = from_email
msg['To'] = to_email

# Send the email using the SMTP server
with smtplib.SMTP(server, port) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_email, msg.as_string())