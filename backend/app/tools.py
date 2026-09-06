# app/tools.py

from app.data import FAKE_DOCUMENT, FAKE_EMAILS, CANARY_SECRETS

def read_document():
    """
    Returns a fake internal company document.
    """
    
    return FAKE_DOCUMENT



def send_email(to, subject, body):
    """
    Simulates sending an email.

    This function DOES NOT send a real email.
    It only prints the email information so we can observe
    what the Honey Agent attempted to do.
    """

    print("\n--- SIMULATED EMAIL ---")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("-----------------------")
    
def read_email(email_id):
    """
    Returns one fake email from the synthetic inbox.
    """

    for email in FAKE_EMAILS:
        if email["id"] == email_id:
            return email

    return "Email not found."    

def get_secret(secret_name):
    """
    Returns one canary secret by name.
    """

    return CANARY_SECRETS.get(
        secret_name,
        "Secret not found."
    )