from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from .utils import *
# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    picture = models.ImageField(upload_to=upload_image_path)
    is_sold = models.BooleanField(default=False)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.BigIntegerField()




    def __str__(self):
        return "{}__{}".format(self.name, self.publisher)


    @property
    def display_name(self):
        og_name = get_file_name(self.picture.name)
        if self.name:
            return self.name
        return og_name


    


class New(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title


class Passwordresetcode(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)  # TODO: do not save password


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)

    def __str__(self):
        return "{}_token".format(self.user)

