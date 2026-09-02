# app/tools.py

from app.data import FAKE_DOCUMENT

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