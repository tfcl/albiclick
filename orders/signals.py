from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from .models import Order

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
import mimetypes
def send_emails(sender,instance, **kwargs):
    print(f"kwargs:{kwargs}")
    print(f"kwargs:{kwargs['update_fields']}")
    state=instance.state


    # if kwargs['created'] and instance.payment:
      
    #     print("Estado=A Aguardar Pagamento")
        
    #     subject = 'Encomenda Albiclick - A Aguardar Pagamento'
    #     html_message = render_to_string('email/1.html', {'order': instance})
    #     plain_message = strip_tags(html_message)
    #     from_email = 'Albiclick'
    #     to = instance.user.email

    #     mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    if kwargs['update_fields']:

        if 'payment' in kwargs['update_fields']:

            print("Estado=A Aguardar Pagamento")
                    
            subject = 'Encomenda Albiclick - A Aguardar Pagamento'
            html_message = render_to_string('email/1.html', {'order': instance})
            plain_message = strip_tags(html_message)
            from_email = 'Albiclick'
            to = instance.user.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        if 'state' in kwargs['update_fields']:

            
            


            if state=="2":
                print("Estado=Pagamento Confirmado")

                subject = 'Encomenda Albiclick - Pagamento confirmado'
                html_message = render_to_string('email/2.html', {'order': instance})
                plain_message = strip_tags(html_message)
                from_email = 'Albiclick'
                to = instance.user.email

                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

                

            elif state=="3":
                print("Estado=A Processar")
                subject = 'Encomenda Albiclick - A Processar'
                html_message = render_to_string('email/3.html', {'order': instance})
                plain_message = strip_tags(html_message)
                from_email = 'Albiclick'
                to = instance.user.email
                
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            elif state=="4":
                print("Estado=Enviado")
                subject = 'Encomenda Albiclick - Enviada'
                html_message = render_to_string('email/4.html', {'order': instance})
                plain_message = strip_tags(html_message)
                from_email = 'Albiclick'
                to = instance.user.email
                email=EmailMessage(subject, html_message, from_email, [to])
                email.content_subtype = "html"

                if instance.invoice:
                    file=instance.invoice
                    content_type=mimetypes.guess_type(file.name)[0]
                    email.attach(file.name, file.read(), content_type)



                email.send()
post_save.connect(send_emails, sender=Order,dispatch_uid="send_emails")


