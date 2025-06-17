from django.core.mail import send_mail

send_mail(
    subject="SMTP2GO Test Email",
    message="This is a test email sent using SMTP2GO with Django.",
    from_email="foxxelab@foxxelabs.com",  # Must match SMTP2GO verified sender or domain
    recipient_list=["todd@toddwriter.com"],  # Replace with your destination email
    fail_silently=False,
)
