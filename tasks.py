from robocorp import workitems
from robocorp import vault
from robocorp.tasks import task

import smtplib
from email.mime.text import MIMEText

import json

from utilities import nltk_helpers as helpers




@task
def get_email_details():
    item = workitems.inputs.current
    print(item)
    email = item.email()

    category_name = categorize_email(subject=email.subject, body=email.text)
    response_text = get_response_to_email(category_name=category_name)
    send_response_to_email(email.from_.address, email.message_id, email.subject, email.text)


def categorize_email(subject, body):
    """Read email content and categorize it."""
    category_name = helpers.categorize_email(subject="", body="")
    return category_name


def get_response_to_email(category_name):
    """Get response text based on a category name."""
    template_map_file = "resources/template_map.json"

    with open(template_map_file, 'r') as file:
        template_map = json.load(file)
    
    template_file_path = template_map.get(category_name)

    if template_file_path:
        try:
            with open(template_file_path, 'r') as template_file:
                return template_file.read()
        except FileNotFoundError:
            print(f"File not found: {template_file_path}")
    else:
        print(f"No template found for category: {category_name}")

    return None


def send_response_to_email(reciever_address, message_id, message_subject, message_text):
    """Send a response to an email."""
    # TODO: SEND IT AS A REPLY INCLUDING SENDER'S EMAIL BODY

    # Credentials are stored in Control Room
    mailbox_credentials = vault.get_secret("mailbox_credentials")
    account_name = mailbox_credentials["name"]
    account_password = mailbox_credentials["password"]

    # Generate a reply
    message = MIMEText(message_text)
    message["From"] = account_name
    message["To"] = reciever_address
    message["Subject"] = f"RE: {message_subject}"

    # Send a reply to sender
    with smtplib.SMTP("smtp.hostinger.com", 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(account_name, account_password)
        smtp_server.sendmail(account_name, reciever_address, message.as_string())