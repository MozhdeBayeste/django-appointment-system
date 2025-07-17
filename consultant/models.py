from django.db import models
from django.contrib.auth.hashers import check_password , make_password

class ConsultantProfile(models.Model):
    full_name = models.CharField(max_length=30, blank=True ,null=True)
    password = models.CharField(max_length=128) 
    email = models.EmailField(unique=True, blank=True ,null=True)
    phoneNumber = models.CharField(max_length=15)
    createdTime = models.DateTimeField(auto_now_add=True)
    specialty = models.CharField(max_length=30)
    experience_years = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.full_name} ,{self.phoneNumber},{self.email},{self.is_active}"

class AvailableTime(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True) 
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.consultant.full_name} , {self.start_time} , {self.end_time} , {self.is_active}"