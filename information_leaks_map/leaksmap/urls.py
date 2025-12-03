from django.urls import path
from .views import (
    check_leaks, user_logout, login_view, register_view, edit_profile,
    view_profile, visualize_breaches, home_view, chronological_journal, help_page,
    get_security_advice, generate_service_security_advice, generate_security_advice_for_breach
)
from . import feedback, reports, support

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('', home_view, name='home'),
    path('check_leaks/', check_leaks, name='check_leaks'),
    path('feedback/', feedback.submit_feedback, name='feedback'),
    path('view_feedback/', feedback.view_feedback, name='view_feedback'),
    path('generate_report/', reports.generate_report, name='generate_report'),
    path('create_ticket/', support.create_ticket, name='create_ticket'),
    path('view_tickets/', support.view_tickets, name='view_tickets'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('view_report/<int:report_id>/', reports.view_report, name='view_report'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('export_report/<int:report_id>/', reports.export_report, name='export_report'),
    path('view_profile/', view_profile, name='view_profile'),
    path('visualize_breaches/', visualize_breaches, name='visualize_breaches'),
    
]
