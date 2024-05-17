from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Role(models.Model):
    role = models.CharField(max_length=100, unique=True)


class UserRole(models.Model):
    status_choice = [("active", "active"), ("disable", "disable")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=20 , choices=status_choice, default='active') 

class UserLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generated = models.DateTimeField(auto_now=True)
    message = models.TextField()
