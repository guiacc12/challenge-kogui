from django.contrib import admin
from django.urls import path, include
from leads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lead_form, name='lead_form'),
    path('leads/', include('leads.urls')),
    path('health/', views.health, name='health'),
]