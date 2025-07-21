from django.db import models
from users.models import UserProfile
from consultant.models import ConsultantProfile ,  AvailableTime


class Appointment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    availableTime = models.OneToOneField(AvailableTime, on_delete=models.CASCADE) 
    bookedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"نوبت {self.id} - {self.consultant.full_name} برای {self.user.full_name} ,{self.status}"