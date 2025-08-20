from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_form, name='lead_form'),
]