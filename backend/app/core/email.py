"""
Email utility functions for sending emails via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send an email via SMTP

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML version of email body
        text_content: Plain text version (optional, falls back to HTML)

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email

        # Add text and HTML parts
        if text_content:
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)

        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_contact_form_email(
    name: str,
    email: str,
    subject: str,
    message: str
) -> bool:
    """
    Send contact form submission to admin

    Args:
        name: Sender's name
        email: Sender's email
        subject: Message subject
        message: Message content

    Returns:
        True if sent successfully
    """
    email_subject = f"[AnotherMe Contact] {subject}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #6366F1; color: white; padding: 20px; text-align: center; }}
            .content {{ background: #f9fafb; padding: 20px; margin: 20px 0; border-radius: 8px; }}
            .field {{ margin-bottom: 15px; }}
            .label {{ font-weight: bold; color: #4b5563; }}
            .value {{ color: #1f2937; }}
            .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>New Contact Form Submission</h2>
            </div>
            <div class="content">
                <div class="field">
                    <div class="label">From:</div>
                    <div class="value">{name}</div>
                </div>
                <div class="field">
                    <div class="label">Email:</div>
                    <div class="value">{email}</div>
                </div>
                <div class="field">
                    <div class="label">Subject:</div>
                    <div class="value">{subject}</div>
                </div>
                <div class="field">
                    <div class="label">Message:</div>
                    <div class="value">{message}</div>
                </div>
            </div>
            <div class="footer">
                <p>This email was sent from the AnotherMe contact form.</p>
                <p>Reply directly to this email to respond to {email}</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
New Contact Form Submission

From: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Reply to: {email}
    """

    return send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=email_subject,
        html_content=html_content,
        text_content=text_content
    )


def send_password_reset_email(
    to_email: str,
    user_name: str,
    reset_token: str
) -> bool:
    """
    Send password reset email to user

    Args:
        to_email: User's email address
        user_name: User's name
        reset_token: Password reset token

    Returns:
        True if sent successfully
    """
    reset_link = f"{settings.FRONTEND_URL}/pages/reset-password.html?token={reset_token}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #6366F1; color: white; padding: 20px; text-align: center; }}
            .content {{ background: #f9fafb; padding: 30px; margin: 20px 0; border-radius: 8px; }}
            .button {{ display: inline-block; background: #6366F1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px; }}
            .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Reset Your Password</h2>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>We received a request to reset your AnotherMe password. Click the button below to create a new password:</p>
                <div style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </div>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #6366F1;">{reset_link}</p>
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul style="margin: 10px 0;">
                        <li>This link expires in 1 hour</li>
                        <li>If you didn't request this, please ignore this email</li>
                        <li>Your password will not change unless you click the link above</li>
                    </ul>
                </div>
            </div>
            <div class="footer">
                <p>This is an automated email from AnotherMe. Please do not reply.</p>
                <p>If you have questions, contact us through the contact form on our website.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
Reset Your AnotherMe Password

Hi {user_name},

We received a request to reset your password. Click the link below to create a new password:

{reset_link}

SECURITY NOTICE:
- This link expires in 1 hour
- If you didn't request this, please ignore this email
- Your password will not change unless you click the link above

---
This is an automated email from AnotherMe.
    """

    return send_email(
        to_email=to_email,
        subject="Reset Your AnotherMe Password",
        html_content=html_content,
        text_content=text_content
    )


def send_verification_email(
    to_email: str,
    user_name: str,
    verification_token: str
) -> bool:
    """
    Send email verification email to user

    Args:
        to_email: User's email address
        user_name: User's name
        verification_token: Email verification token

    Returns:
        True if sent successfully
    """
    verification_link = f"{settings.FRONTEND_URL}/pages/verify-email.html?token={verification_token}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #6366F1; color: white; padding: 20px; text-align: center; }}
            .content {{ background: #f9fafb; padding: 30px; margin: 20px 0; border-radius: 8px; }}
            .button {{ display: inline-block; background: #6366F1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px; }}
            .info {{ background: #dbeafe; border-left: 4px solid #3b82f6; padding: 12px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Welcome to AnotherMe!</h2>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>Thank you for signing up for AnotherMe, the birthday social network! To complete your registration, please verify your email address by clicking the button below:</p>
                <div style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Email Address</a>
                </div>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #6366F1;">{verification_link}</p>
                <div class="info">
                    <strong>ℹ️ What's Next:</strong>
                    <ul style="margin: 10px 0;">
                        <li>Click the verification link above</li>
                        <li>Complete your profile</li>
                        <li>Find your birthday twins</li>
                        <li>Start connecting with others!</li>
                    </ul>
                </div>
                <p style="color: #6b7280; font-size: 14px; margin-top: 20px;">This link will expire in 24 hours.</p>
            </div>
            <div class="footer">
                <p>This is an automated email from AnotherMe. Please do not reply.</p>
                <p>If you didn't create an account, you can safely ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
Welcome to AnotherMe!

Hi {user_name},

Thank you for signing up for AnotherMe, the birthday social network! To complete your registration, please verify your email address by clicking the link below:

{verification_link}

This link will expire in 24 hours.

What's Next:
- Click the verification link above
- Complete your profile
- Find your birthday twins
- Start connecting with others!

---
This is an automated email from AnotherMe.
If you didn't create an account, you can safely ignore this email.
    """

    return send_email(
        to_email=to_email,
        subject="Verify Your AnotherMe Email Address",
        html_content=html_content,
        text_content=text_content
    )
