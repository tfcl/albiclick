from django.db.models.signals import post_save, post_init,pre_save
from .models import Profile
from orders.models import Order





def adress_update(sender,instance, **kwargs):
    print("from profile signal")
    print(f"kwargs:{kwargs}")
    if kwargs['update_fields']:
        if 'adress' in kwargs['update_fields']:
            
            old_instance=Profile.objects.get(pk=instance.pk)
            adress=old_instance.adress

            if adress:
                print(adress.pk)
            
                if not Order.objects.filter(adress=adress).exists():
                    old_instance.adress=None
                    old_instance.save()
                    adress.delete()

        elif 'adress_billing' in kwargs['update_fields']:
            old_instance=Profile.objects.get(pk=instance.pk)
            adress=old_instance.adress_billing

            if adress:
                print(adress.pk)
            
                if not Order.objects.filter(adress_billing=adress).exists():
                    old_instance.adress_billing=None
                    old_instance.save()
                    adress.delete()
pre_save.connect(adress_update, sender=Profile,dispatch_uid="adress_update")
