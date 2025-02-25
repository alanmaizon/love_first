from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def generate_donation_receipt(user_name, amount):
    """Generate a PDF receipt for the donation."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Donation Receipt")
    p.drawString(100, 730, f"Donor Name: {user_name}")
    p.drawString(100, 710, f"Donation Amount: ${amount}")
    p.drawString(100, 690, "Thank you for your generous support!")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def send_donation_email(user_email, user_name, amount):
    """Send an HTML donation receipt email with a PDF attachment."""
    subject = "🎉 Thank You for Your Donation!"
    html_content = render_to_string("emails/donation_email.html", {
        "name": user_name,
        "amount": amount
    })
    text_content = strip_tags(html_content)  # Fallback for plain-text email clients

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email])
    email.attach_alternative(html_content, "text/html")

    # Generate PDF receipt
    pdf_buffer = generate_donation_receipt(user_name, amount)
    email.attach("Donation_Receipt.pdf", pdf_buffer.getvalue(), "application/pdf")

    email.send()