# app/tools.py

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