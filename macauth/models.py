from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


class MacAddr(models.Model):
    position = models.CharField(max_length=32,default='shanghai')
    macaddr = models.CharField(max_length=32)
