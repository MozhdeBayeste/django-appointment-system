from django.db import models
from users.models import UserProfile
from consultant.models import ConsultantProfile ,  AvailableTime


class Appointmnet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    available_time = models.OneToOneField(AvailableTime, on_delete=models.CASCADE) 
    status_choices = [
        ('pending', 'در انتظار '),
        ('confirmed', 'تایید شده'),
        ('cancelled', 'کنسل شده'),
        ('done', 'انجام شده'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"نوبت {self.id} - {self.consultant.full_name} برای {self.user.full_name} ,{self.status}"