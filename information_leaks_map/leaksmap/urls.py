from django.urls import path
from .views import (
    check_leaks, user_logout, user_login, register, edit_profile,
    view_profile, visualize_breaches, home, chronological_journal, help_page,
    get_security_advice, generate_service_security_advice, generate_security_advice_for_breach
)
from . import feedback, reports, support

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('check_leaks/', check_leaks, name='check_leaks'),
    path('feedback/', feedback.submit_feedback, name='feedback'),
    path('view_feedback/', feedback.view_feedback, name='view_feedback'),
    path('generate_report/', reports.generate_report, name='generate_report'),
    path('create_ticket/', support.create_ticket, name='create_ticket'),
    path('view_tickets/', support.view_tickets, name='view_tickets'),
    path('view_report/<int:report_id>/', reports.view_report, name='view_report'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('export_report/<int:report_id>/', reports.export_report, name='export_report'),
    path('view_profile/', view_profile, name='view_profile'),
    path('visualize_breaches/', visualize_breaches, name='visualize_breaches'),
    path('chronological_journal/', chronological_journal, name='chronological_journal'),
    path('help/', help_page, name='help'),
    path('get_security_advice/', get_security_advice, name='get_security_advice'),
    path('generate_service_security_advice/', generate_service_security_advice, name='generate_service_security_advice'),
    path('generate_security_advice_for_breach/', generate_security_advice_for_breach, name='generate_security_advice_for_breach'),
]
