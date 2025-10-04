from django.urls import path
from . import views, feedback, reports, support
from .views import export_report, visualize_breaches

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
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_report/', views.view_report, name='view_report'),
]
