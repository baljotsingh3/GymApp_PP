# from Member.models import Payment
# from io import BytesIO
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from django.http import HttpResponse


# from django.core.mail import EmailMessage
# from django.conf import settings
# from io import BytesIO


# class EmailService:
#     """
#     Utility class for sending emails with or without attachments.
#     """

#     def __init__(self, from_email=None):
#         # Default to Django's DEFAULT_FROM_EMAIL
#         self.from_email = from_email or settings.DEFAULT_FROM_EMAIL

#     def send_simple_email(self, subject, body, to_emails):
#         """
#         Send a plain text email.
#         """
#         email = EmailMessage(
#             subject=subject,
#             body=body,
#             from_email=self.from_email,
#             to=to_emails if isinstance(to_emails, list) else [to_emails],
#         )
#         email.send(fail_silently=False)

#     def send_email_with_attachment(self, subject, body, to_emails, filename, file_content, mime_type):
#         """
#         Send an email with an attachment (PDF, CSV, etc.).
#         """
        
#         email = EmailMessage(
#             subject=subject,
#             body=body,
#             from_email=self.from_email,
#             to=to_emails if isinstance(to_emails, list) else [to_emails],
#         )
#         email.attach(filename, file_content, mime_type)
#         email.send(fail_silently=False)

#     def send_invoice_email(self, to_email, pdf_buffer: BytesIO, order_id):
#         """
#         Shortcut for sending a PDF invoice email.
#         """
#         subject = f"Invoice for Order {order_id}"
#         body = (
#             f"Dear Customer,\n\n"
#             f"Please find attached your invoice for order {order_id}.\n\n"
#             f"Thank you for your purchase!"
#         )

#         filename = f"invoice_{order_id}.pdf"
#         return self.send_email_with_attachment(
#             subject,
#             body,
#             [to_email],
#             filename,
#             pdf_buffer.getvalue(),
#             "application/pdf",
#         )

# class InvoiceGenerator:
#     def __init__(self, order_id, customer_name, amount):
#         self.order_id = order_id
#         self.customer_name = customer_name
#         self.amount = amount

#     def generate_pdf(self):
#         """
#         Returns an HttpResponse with PDF content.
#         """
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer, pagesize=A4)
#         width, height = A4

#         # Header
#         p.setFont("Helvetica-Bold", 16)
#         p.drawString(200, height - 50, "Payment Invoice")

#         # Body
#         p.setFont("Helvetica", 12)
#         p.drawString(100, height - 100, f"Order ID: {self.order_id}")
#         p.drawString(100, height - 120, f"Customer: {self.customer_name}")
#         p.drawString(100, height - 140, f"Amount Paid: ₹{self.amount:.2f}")

#         # Footer
#         p.setFont("Helvetica-Oblique", 10)
#         p.drawString(100, 100, "Thank you for your payment!")

#         # Finalize
#         p.showPage()
#         p.save()

#         buffer.seek(0)
#         response = HttpResponse(buffer, content_type="application/pdf")
#         response['Content-Disposition'] = f'attachment; filename="invoice_{self.order_id}.pdf"'
#         return response



# 



from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class InvoiceGenerator:
    """
    Generates a PDF invoice for a given order.
    """

    def __init__(self, order_id, customer_name, amount):
        self.order_id = order_id
        self.customer_name = customer_name
        self.amount = amount

    def generate_pdf_buffer(self):
        """
        Generate invoice and return it as BytesIO buffer.
        """
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Header
        p.setFont("Helvetica-Bold", 18)
        p.drawString(200, height - 50, "Payment Invoice")

        # Invoice details
        p.setFont("Helvetica", 12)
        p.drawString(100, height - 120, f"Order ID: {self.order_id}")
        p.drawString(100, height - 140, f"Customer: {self.customer_name}")
        p.drawString(100, height - 160, f"Amount Paid: ₹{self.amount:.2f}")

        # Footer
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(100, 100, "Thank you for your payment!")

        # Finalize PDF
        p.showPage()
        p.save()
        buffer.seek(0)

        return buffer

    def get_http_response(self):
        """
        Generate invoice and return as downloadable HTTP response.
        """
        buffer = self.generate_pdf_buffer()
        response = HttpResponse(buffer, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="invoice_{self.order_id}.pdf"'
        return response


class EmailService:
    """
    Utility class for sending emails (simple, with attachments, or invoices).
    """

    def __init__(self, from_email=None):
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL

    #for contact forms
    def send_simple_email(self, subject, body):
        """
        Send a plain text email.
        """
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=self.from_email,
            to= ["jotdhillon2002@gmail.com"],
        )
        email.send(fail_silently=False)

    def send_email_with_attachment(self, subject, body, to_emails, filename, file_content, mime_type):
        """
        Send an email with an attachment.
        """
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=self.from_email,
            to=to_emails if isinstance(to_emails, list) else [to_emails],
        )
        email.attach(filename, file_content, mime_type)
        email.send(fail_silently=False)

    def send_invoice_email(self, to_email, invoice_buffer: BytesIO, order_id):
        """
        Send invoice PDF as email attachment.
        """
        subject = f"Invoice for Order {order_id}"
        body = (
            f"Dear Customer,\n\n"
            f"Please find attached your invoice for order {order_id}.\n\n"
            f"Thank you for your purchase!"
        )

        filename = f"invoice_{order_id}.pdf"
        self.send_email_with_attachment(
            subject,
            body,
            [to_email],
            filename,
            invoice_buffer.getvalue(),
            "application/pdf",
        )
