import razorpay  # or stripe/paypal
from django.conf import settings

from Member.models import Payment
# Example for Razorpay



class PaymentGateway:
    """Handles payment creation and verification using Razorpay API."""

    def __init__(self):
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    def create_order(self, amount, currency="INR", receipt=None):
        """
        Create a payment order in Razorpay.
        """
        order = self.client.order.create({
            "amount": int(amount),  # Razorpay expects amount in paisa
            "currency": currency,
            "receipt": receipt or "receipt_1",
            "payment_capture": 1
        })
        return order

    def verify_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verify the payment signature sent by Razorpay.
        """
        try:
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
            return self.client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            return False
    
    
    def record_payment(self, user, payment_id, amount, currency, status, order_id=None):
        
        return Payment.objects.create(
            user=user,
            payment_id=payment_id,
            order_id=order_id,
            amount=amount,
            currency=currency,
            status=status
        )
