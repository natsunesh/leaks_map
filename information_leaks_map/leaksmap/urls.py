from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check_leaks/', views.check_leaks, name='check_leaks'),
    path('export_report/', views.export_report, name='export_report'),
]
