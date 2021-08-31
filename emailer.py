from RPA.Email.ImapSmtp import ImapSmtp
from RPA.Robocorp.Vault import Vault


def send_email(recipient, subject, body):
    secret = Vault().get_secret("emailCredentials")
    gmail_account = secret["username"]
    gmail_password = secret["password"]
    mail = ImapSmtp(smtp_server="smtp.gmail.com", smtp_port=587)
    mail.authorize(account=gmail_account, password=gmail_password)
    mail.send_message(
        sender=gmail_account,
        recipients=recipient,
        subject=subject,
        body=body,
    )
