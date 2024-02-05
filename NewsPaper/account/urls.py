from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import IndexView, upgrade_me

urlpatterns = [
    path('personal/', IndexView.as_view(), name='personal_account'),
    path('personal/upgrade/', upgrade_me, name='upgrade')

]