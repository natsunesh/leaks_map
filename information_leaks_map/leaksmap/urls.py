from django.urls import path
from .views import check_leaks, user_logout as user_logout, user_login as user_login
from . import feedback, reports, visualizer
from . import support

urlpatterns = [
path('logout/', user_logout, name='logout'),
    path('', check_leaks, name='home'),
    path('check_leaks/', check_leaks, name='check_leaks'),
    path('feedback/', feedback.submit_feedback, name='feedback'),
    path('view_feedback/', feedback.view_feedback, name='view_feedback'),
    path('generate_report/', reports.generate_report, name='generate_report'),
    path('create_ticket/', support.create_ticket, name='create_ticket'),
    path('view_tickets/', support.view_tickets, name='view_tickets'),
path('view_report/', reports.view_report, name='view_report'),
path('login/', user_login, name='login'),
path('logout/', user_logout, name='logout'),
]
