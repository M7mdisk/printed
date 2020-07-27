#from django.db import models
from django.contrib.gis.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django_extensions.db.fields import ShortUUIDField
from django.contrib.auth.models import User, BaseUserManager
import shortuuid
import PyPDF2, io, requests
from urllib.parse import unquote


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    isOwner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return self.name

def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.pdf','.doc','.docx','.png','.jpg','.jpeg']
  if not ext in valid_extensions:
    raise ValidationError(u'File not supported!')

import os
def file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "media/%s/%s_%s.%s" % (instance.shop.name,instance.shop.name,instance.uuid, ext)
    return os.path.join('uploads', filename)

class Order(models.Model):
    uuid = ShortUUIDField(primary_key=True)
    buyer = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='buyer')
    date = models.DateTimeField(auto_now_add=True)
    docfile = models.FileField(upload_to=file_name,validators=[validate_file_extension])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1)
    type = models.ForeignKey(Type,on_delete=models.CASCADE, related_name='printtype',default=0)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='shop')
    total = models.DecimalField(max_digits=6,decimal_places=3,editable=False)
    SIZE_CHOICES = (("A4","A4"),("A3","A3"),('A2','A2'))
    notes = models.TextField(blank=True,max_length=300, default='')
    size = models.CharField(max_length=9,
                  choices=SIZE_CHOICES,
                  default="A4")  
    status = models.CharField(max_length=9,
                  default="On Queue")
    def save(self, *args, **kwargs):
        if not self.total:
            ext = os.path.splitext(self.docfile.url)[1]
            if ext == '.pdf':
                pdf = PyPDF2.PdfFileReader(self.docfile)
                npages = pdf.getNumPages()
                self.total = self.quantity * npages * Type.objects.filter(name=self.type).first().price
            else:
                self.total = self.quantity * Type.objects.filter(name=self.type).first().price
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.uuid)
    def extension(self):
        name, extension = os.path.splitext(self.docfile.name)
        return extension