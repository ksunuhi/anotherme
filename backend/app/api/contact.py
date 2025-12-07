"""
Contact form API endpoints
"""
from fastapi import APIRouter, HTTPException, status

from app.schemas.contact import ContactFormRequest, ContactFormResponse
from app.core.email import send_contact_form_email

router = APIRouter()


@router.post("/", response_model=ContactFormResponse)
async def submit_contact_form(form_data: ContactFormRequest):
    """
    Submit contact form and send email to admin

    Args:
        form_data: Contact form data (name, email, subject, message)

    Returns:
        Success response

    Raises:
        HTTPException: If email fails to send
    """
    # Send email to admin
    success = send_contact_form_email(
        name=form_data.name,
        email=form_data.email,
        subject=form_data.subject,
        message=form_data.message
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send contact form. Please try again later."
        )

    return ContactFormResponse(
        success=True,
        message="Thank you for contacting us! We'll get back to you soon."
    )
