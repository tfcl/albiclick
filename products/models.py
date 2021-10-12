from django.db import models
from tinymce.models import HTMLField 

def product_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    print(f"Intance on model path: {instance}")
    return 'product_{id}/{filename}'.format(id=instance.pk, filename=filename)


    return "user_{id}/{file}".format(id=instance.user.id, file=filename)

class Category(models.Model):
    name=models.CharField(max_length=100)
    parentPk=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    depth=models.IntegerField(default=0)
    udc=models.IntegerField()
    def __str__(self):
        return self.name



class Product(models.Model):
    name= models.CharField(max_length=120)
    description=models.TextField(max_length=1000)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    avalability=models.BooleanField(default=True)
    highlighted=models.BooleanField(default=False)
    new=models.BooleanField(default=False)
    stock=models.IntegerField()
    category=models.ForeignKey(Category,null=True, on_delete=models.CASCADE)
    main_image=models.ImageField(upload_to = product_directory_path, default='default.jpg')
    detail=HTMLField(null=True)
# Create your models here.

class Spec(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name= models.CharField(max_length=120)
    spec= models.CharField(max_length=120)



class Image(models.Model):
    image=models.ImageField()
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)