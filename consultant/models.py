from django.db import models
from django.contrib.auth.hashers import check_password , make_password

class ConsultantProfile(models.Model):
    fullName = models.CharField(max_length=30, blank=True ,null=True)
    password = models.CharField(max_length=128) 
    email = models.EmailField(unique=True, blank=True ,null=True)
    phoneNumber = models.CharField(max_length=15)
    createdTime = models.DateTimeField(auto_now_add=True)
    specialty = models.CharField(max_length=30)
    isActive = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.fullName} ,{self.phoneNumber},{self.email},{self.isActive}"

class AvailableTime(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    isActive = models.BooleanField(default=True) 
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.consultant.fullName} , {self.startTime} , {self.endTime} , {self.isActive}"