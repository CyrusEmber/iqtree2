import logging
import smtplib, ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

import yaml

from logger import gen_log

logger = gen_log("test")
# Parse command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--to', dest='to_email', help='the email receiver')
parser.add_argument('-r', '--result', dest='result', help='the result yaml file')
parser.add_argument('-g', '--github_repo', dest='repository', help='github repository')
# parser.add_argument('-i', '--image', dest='image', help='the result image')


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
email_subject = 'Github Action Result'
email_body = ''
msg = MIMEMultipart()

# Access the options
if args.to_email:
    logger.info(f'Send email to: {args.to_email}')
    to_email = args.to_email
else:
    logger.error("No email specified")


# Access the log file and concatenate it to the email body
# find log file that is in the same directory as this script
for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    if file.endswith(".log"):
        # print(file)
        pass

# Attach file
with open(args.result, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {args.result}",
    )
    msg.attach(part)

    # Set subject
    data = yaml.safe_load(args.result)
    # Count failure tests
    failed_tests = 0
    passed_tests = 0
    for command in data:
        if command["result"] == "Passed":
            passed_tests += 1
        else:
            failed_tests += 1
    if failed_tests > 0:
        email_subject = f'Failed {failed_tests} tests for {args.repository}'
    else:
        email_subject = f'Passed all tests for {args.repository}'

    # Set body
    # email_body = f'Please find the result attached'


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
    server.quit()

print("Email sent successfully!")