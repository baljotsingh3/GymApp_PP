from rest_framework.authtoken.models import Token


from django.core.mail import EmailMessage
from Member.payment.services import EmailService



class TokenGenerator(EmailService):
    
    def send_token_email(self,user):
        token, created = Token.objects.get_or_create(user= user)
        subject = "Your API Token"
        message = f"Hello {user.username},\n\nHere is your API token:\n\n{token.key}\n\nUse this in your API requests."
        
        email = EmailMessage(
                        subject=subject,
                        body=message,
                        from_email=self.from_email,
                        to= ["jotdhillon2002@gmail.com"],  
                    )
        email.send(fail_silently=False)
        
        return token.key
