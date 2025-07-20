from django.shortcuts import render
from consultant.models import ConsultantProfile
from django.db.models import Q
from django.views import View
    
class HomeView(View):
    def get(self,request):
        query = request.GET.get('q')
        consultants = ConsultantProfile.objects.all()

        if query:
            consultants = consultants.filter(Q(full_name__icontains=query) | Q(specialty__icontains=query))

        consultants = consultants[:24]

        return render(request, 'main/home.html', {'consultants': consultants})