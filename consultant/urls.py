from django.urls import path
from . import views

urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='consultant_login'),
    path('update/',views.ConsultantUpdateView.as_view(),name='consultant_update'),
    path('add-availabletime/',views.AddAvailableTimeView.as_view(),name='add_availabletime'),
    path('<int:pk>/', views.ConsultantProfileView.as_view(), name='consultant_profile'),
    path('dashboard/', views.ConsultantDashboardView.as_view(), name='consultant_dashboard'),
    path('consultant-list/', views.ConsultantListView.as_view(), name='consultant_list'),
    path('availabletimes/', views.AvailableTimeListView.as_view(), name='consultant_available_times'),
    path('appointments/', views.AppointmentListView.as_view(), name='consultant_appointments'),
]