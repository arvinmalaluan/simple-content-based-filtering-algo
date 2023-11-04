from django.db import models

# Create your models here.


class Role(models.Model):
    role = models.CharField(max_length=50)


class Account(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100, default='allowed', null=True, blank=True)
    role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
