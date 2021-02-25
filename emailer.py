from RPA.Email.ImapSmtp import ImapSmtp
from RPA.Robocloud.Secrets import Secrets

secrets = Secrets()
secret = secrets.get_secret("emailCredentials")
gmail_account = secret["username"]
gmail_password = secret["password"]


def send_email(recipient, subject, body):
    mail = ImapSmtp(smtp_server="smtp.gmail.com", smtp_port=587)
    mail.authorize(account=gmail_account, password=gmail_password)
    mail.send_message(
        sender=gmail_account,
        recipients=recipient,
        subject=subject,
        body=body,
    )
