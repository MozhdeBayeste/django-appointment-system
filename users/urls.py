from django.urls import path
from . import views

urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='user_login'),
    path('update/',views.UserUpdateView.as_view(),name='user_update'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('my-appointments/', views.UserAppointmentsView.as_view(), name='user_appointments'),
    path('consultant/<int:consultant_id>/times/',views.ConsultantAvailableTimesView.as_view(), name='reservation_list'),

]