
from django.db import models
from django.contrib.auth.hashers import check_password , make_password

class UserProfile(models.Model):
    username = models.CharField(max_length=30, blank=True ,null=True)
    password = models.CharField(max_length=128) 
    fullName = models.CharField(max_length=30, blank=True ,null=True)
    email = models.EmailField(unique=True, blank=True ,null=True)
    phoneNumber = models.CharField(max_length=15)
    createdTime = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.username} ,{self.phoneNumber},{self.email},{self.fullName}"