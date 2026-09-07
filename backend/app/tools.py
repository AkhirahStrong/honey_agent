# app/tools.py

from app.data import (
    FAKE_DOCUMENTS,
    FAKE_EMAILS,
    CANARY_SECRETS,
    FAKE_EMPLOYEES,
    FAKE_CUSTOMERS,
    FAKE_INVOICES,
    FAKE_SUPPORT_TICKETS,
    FAKE_COMPANY,
    ROLE_PERMISSIONS
)

def read_document(document_id):
    """
    Returns one fake document by document ID.
    """

    for document in FAKE_DOCUMENTS:
        if document["document_id"] == document_id:
            return document

    return "Document not found."



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
    
def get_employee(employee_id):
    """
    Returns one fake employee record by employee ID.
    """

    for employee in FAKE_EMPLOYEES:
        if employee["employee_id"] == employee_id:
            return employee

    return "Employee not found."    

def get_customer(customer_id):
    """
    Returns one fake customer record by customer ID.
    """

    for customer in FAKE_CUSTOMERS:
        if customer["customer_id"] == customer_id:
            return customer

    return "Customer not found."

def get_ticket(ticket_id):
    """
    Returns one fake support ticket by ticket ID.
    """

    for ticket in FAKE_SUPPORT_TICKETS:
        if ticket["ticket_id"] == ticket_id:
            return ticket

    return "Ticket not found."

def get_invoice(invoice_id):
    """
    Returns one fake invoice by invoice ID.
    """

    for invoice in FAKE_INVOICES:
        if invoice["invoice_id"] == invoice_id:
            return invoice

    return "Invoice not found."

def get_company_profile():
    """
    Returns the fake company information.
    """

    return FAKE_COMPANY

def get_role_permissions(role_name):
    """
    Returns the permissions assigned to a fake company role.
    """

    return ROLE_PERMISSIONS.get(
        role_name,
        "Role not found."
    )