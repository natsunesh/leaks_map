from django.urls import path
from .views import check_leaks, user_logout, user_login, register, edit_profile, view_profile
from . import feedback, reports, visualizer, support



urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('', check_leaks, name='home'),
    path('feedback/', feedback.submit_feedback, name='feedback'),
    path('view_feedback/', feedback.view_feedback, name='view_feedback'),
    path('generate_report/', reports.generate_report, name='generate_report'),
    path('create_ticket/', support.create_ticket, name='create_ticket'),
    path('view_tickets/', support.view_tickets, name='view_tickets'),
    path('view_report/', reports.view_report, name='view_report'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('export_report/', reports.export_report, name='export_report'),
    path('view_profile/', view_profile, name='view_profile'),
    path('visualize_breaches/', visualizer.visualize_breaches, name='visualize_breaches'),
]
