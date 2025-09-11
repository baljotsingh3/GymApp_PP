from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment
from Member.payment import services   


from django.dispatch import receiver
from .models import Payment, Member, Invoice

from django.dispatch import Signal 





order_created = Signal()

@receiver(order_created)
def create_payment_entry(request, order, **kwargs):
    
    amount = order.get("amount")

    member = Member.objects.get(user=request.user)  # assuming Member has OneToOne with User
    plan = member.plan

    if member:
        print("Payment record is going to dump in db")
        try:
            payment = Payment.objects.create(
                member=member,
                plan=plan,
                amount=amount / 100,
                status="Paid",
                order_id=order["id"]
            )
            print("Payment saved:", payment)
        except Exception as e:
            print("Payment save failed:", e)
        print("done")
        
        
        return True
        

# @receiver(post_save, sender=Payment)
# def send_invoice_on_payment(sender, instance, created, **kwargs):
#     if created and instance.status == "Paid":  # Only new + successful payments
#         member = instance.member
        
#         print("invoice generator")
        
        
#         invoice = services.InvoiceGenerator(
#             order_id=instance.order_id or instance.payment_id,
#             customer_name=member.user.get_full_name() or member.user.username,
#             amount=instance.amount
#         )

#         pdf_buffer = invoice.generate_pdf_buffer()  # should return BytesIO or file path


#         print("pdf_generated") 
        
        
#         email = services.EmailService()
#         email.send_invoice_email(
#             to_email= "jotdhillon2002@gmail.com",
#             invoice_buffer= pdf_buffer,
#             order_id=instance.order_id or instance.payment_id,
#         )
       
#         return True
    
    
 

@receiver(post_save, sender=Payment)
def send_invoice_on_payment(sender, instance, created, **kwargs):
    if created and instance.status == "Paid":  # Only new + successful payments
        member = instance.member
        print("invoice generator")

        # Generate PDF invoice
        invoice = services.InvoiceGenerator(
            order_id=instance.order_id or instance.payment_id,
            customer_name=member.user.get_full_name() or member.user.username,
            amount=instance.amount
        )
        pdf_buffer = invoice.generate_pdf_buffer()  # should return BytesIO

        print("pdf_generated")

        # Save PDF into Invoice model
        invoice_record = Invoice.objects.create(payment=instance)
        invoice_record.pdf_file.save(
            f"invoice_{instance.order_id or instance.payment_id}.pdf", 
            ContentFile(pdf_buffer.getvalue()),  # wrap BytesIO in ContentFile
            save=True
        )

        # Send email with the invoice attached
        email = services.EmailService()
        email.send_invoice_email(
            to_email= "jotdhillon2002@gmail.com",  # <-- use member’s real email
            invoice_buffer=pdf_buffer,
            order_id=instance.order_id or instance.payment_id,
        )

        return True
