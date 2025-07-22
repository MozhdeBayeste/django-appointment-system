from django.shortcuts import render
from consultant.models import ConsultantProfile , AvailableTime
from django.db.models import Q
from django.views import View
from django.utils.timezone import now

def remove_expired_available_times():
    AvailableTime.objects.filter(startTime__lt=now(), isActive=True).delete()

    
class HomeView(View):
    def get(self,request):
        remove_expired_available_times()
        query = request.GET.get('q')
        consultants = ConsultantProfile.objects.all()

        if query:
            consultants = consultants.filter(Q(fullName__icontains=query) | Q(specialty__icontains=query))

        consultants = consultants[:24]

        return render(request, 'main/home.html', {'consultants': consultants})