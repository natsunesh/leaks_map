from django.urls import path
from . import views, feedback, reports, support

urlpatterns = [
    path('', views.home, name='home'),
    path('check_leaks/', views.check_leaks, name='check_leaks'),
    path('export_report/', views.export_report, name='export_report'),
    path('visualize_breaches/', views.visualize_breaches, name='visualize_breaches'),
    path('feedback/', feedback.submit_feedback, name='feedback'),
    path('view_feedback/', feedback.view_feedback, name='view_feedback'),
    path('generate_report/', reports.generate_report, name='generate_report'),
    path('create_ticket/', support.create_ticket, name='create_ticket'),
    path('view_tickets/', support.view_tickets, name='view_tickets'),
]
