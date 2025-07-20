from django.urls import path
from . import views

urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='user-login'),
    path('user-update/',views.UserUpdateView.as_view(),name='user_update'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard')

]