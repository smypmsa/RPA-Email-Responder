from robocorp import workitems
from robocorp import vault
from robocorp.tasks import task

import smtplib
from email.mime.text import MIMEText

from utilities import categorize_text as email_categorization
from utilities import get_response_text as email_response




@task
def categorize_email():
    """Read email content and categorize it."""

    # Get item's details
    item = workitems.inputs.current
    email = item.email()

    # Assign a category to this item (email)
    category_name = email_categorization.categorize_email(subject=email.subject, body=email.text)
    
    # Get a response for this category
    response_text = email_response.get_response_text(category_name=category_name, customer_name=email.from_.name)
    if not response_text:
        raise Exception(f"Response text not found.")

    # Get credentials from Control Room
    mailbox_credentials = vault.get_secret("mailbox_credentials")
    account_name = mailbox_credentials["name"]
    account_password = mailbox_credentials["password"]

    # Set a recipient, sender and subject
    recipient_address = email.from_.address
    sender_address = account_name
    if not email.subject.lower().startswith("re:"):
        subject = f"RE: {email.subject}"
    else:
        subject = email.subject

    # Format original message
    formatted_original_message = f"\n\nFrom: {email.from_.address}\nDate: {str(email.date)}\nSubject: {email.subject}\nMessage:\n{email.text}"

    # Generate a message
    message = MIMEText(response_text + formatted_original_message)
    message["From"] = sender_address
    message["To"] = recipient_address
    message["Subject"] = subject
    message["In-Reply-To"] = email.message_id
    message["References"] = email.message_id

    # Send a message as a reply
    with smtplib.SMTP("smtp.hostinger.com", 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(account_name, account_password)
        smtp_server.sendmail(sender_address, recipient_address, message.as_string())