from django.urls import path
from . import views

urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='login_consultant'),
    path('consultant-update/',views.ConsultantUpdateView.as_view(),name='consultant_update'),
    path('add-availabletime/',views.AddAvailableTimeView.as_view(),name='add_availabletime'),


]