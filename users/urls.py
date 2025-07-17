from django.urls import path
from . import views

urlpatterns = [
    path('reg/',views.RegistrationView.as_view(),name='login'),
    path('user-update/',views.UserUpdateView.as_view(),name='user_update'),

]