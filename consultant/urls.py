from django.urls import path
from . import views

urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='consultant-login'),
    path('consultant-update/',views.ConsultantUpdateView.as_view(),name='consultant_update'),
    path('add-availabletime/',views.AddAvailableTimeView.as_view(),name='add_availabletime'),
    path('<int:pk>/', views.ConsultantProfileView.as_view(), name='consultant-profile'),
    path('dashboard/', views.ConsultantDashboardView.as_view(), name='dashboard'),


]