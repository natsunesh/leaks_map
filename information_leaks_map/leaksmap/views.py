from typing import List
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
import asyncio
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.utils import timezone
import os
from .api_client import LeakCheckAPIClient
from .models import Breach
from .forms import (
    RegistrationForm, LoginForm, BreachCheckForm, ReportExportForm, BreachFilterForm
)
import logging

logger = logging.getLogger(__name__)

# ========== AUTH VIEWS ==========
def login_view(request):
    """Обработка авторизации."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Добро пожаловать!')
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    """Обработка регистрации."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_logout(request):
    """Выход из системы."""
    logout(request)
    messages.success(request, 'Вы успешно вышли')
    return redirect('home')

# ========== MAIN VIEWS ==========
@login_required
def index(request):
    check_form = BreachCheckForm()
    export_form = ReportExportForm()

    if request.method == "POST":
        # Нажата кнопка "Проверить утечки"
        if "check_breaches" in request.POST:
            check_form = BreachCheckForm(request.POST)
            if check_form.is_valid():
                email = check_form.cleaned_data["email"]
                # ВАЖНО: редирект на страницу визуализации с email в query
                url = reverse("visualize_breaches")
                return redirect(f"{url}?email={email}")

        # Нажата кнопка "Экспортировать отчет"
        if "export_report" in request.POST:
            export_form = ReportExportForm(request.POST)
            if export_form.is_valid():
                # Здесь можешь использовать mock-генерацию отчета
                response = generate_mock_report({
                    'format': export_form.cleaned_data['format'],
                    'email': export_form.cleaned_data['email']
                })
                return response
            else:
                messages.error(request, 'Ошибка в форме экспорта отчета.')

    context = {
        "check_form": check_form,
        "export_form": export_form,
    }
    return render(request, "leaksmap/home.html", context)

# Mock-генерация отчета
def generate_mock_report(data):
    format_type = data['format']
    email = data['email']

    if format_type == 'pdf':
        # Создание PDF отчета (mock)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{email}.pdf"'
        response.write(f"PDF Report for {email}")
        return response
    else:
        # Создание HTML отчета (mock)
        html_content = f"""
        <!DOCTYPE html>
        <html><head><title>Отчет</title></head>
        <body>
            <h1>Отчет об утечках для {email}</h1>
            <p>Это тестовый отчет в формате HTML.</p>
        </body></html>
        """
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="report_{email}.html"'
        return response

# ========== API ENDPOINTS ==========
@login_required
@csrf_protect
@require_http_methods(["POST"])
def api_check_leaks(request):
    """AJAX проверка утечек (исправлена async проблема)."""
    form = BreachCheckForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": dict(form.errors)}, status=400)

    email = form.cleaned_data['email']
    api_key = os.getenv('LEAKCHECK_API_KEY')

    if not api_key:
        return JsonResponse({"error": "API ключ не настроен"}, status=500)

    try:
        client = LeakCheckAPIClient(api_key)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        breaches_data = asyncio.run(client.get_breach_info_by_email(email))
        loop.close()

        if not breaches_data:
            return JsonResponse({
                "status": "success",
                "count": 0,
                "message": "Утечки не найдены",
                "checklist": generate_checklist([])
            })

        # Сохраняем утечки
        saved_breaches = []
        for data in breaches_data:
            breach, created = Breach.objects.update_or_create(
                user=request.user,
                service_name=data["service_name"],
                defaults={
                    'breach_date': data.get("breach_date"),
                    'location': data.get("location", "Unknown"),
                    'data_type': data.get("data_type", ""),
                    'description': data.get("description", ""),
                    'source': data.get("source", "")
                }
            )
            saved_breaches.append(breach)

        return JsonResponse({
            "status": "success",
            "count": len(breaches_data),
            "breaches": breaches_data,
            "checklist": generate_checklist(saved_breaches)
        })

    except Exception as e:
        logger.error(f"API error: {e}")
        return JsonResponse({"error": "Ошибка проверки API"}, status=500)

@login_required
@require_http_methods(["POST"])
def api_export_report(request):
    """AJAX экспорт отчета (убрано render_to_string)."""
    form = ReportExportForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": dict(form.errors)}, status=400)

    format_type = form.cleaned_data['format']
    breaches = list(Breach.objects.filter(user=request.user).values(
        'service_name', 'breach_date', 'data_type', 'description'
    )[:50])

    html_content = f"""
    <!DOCTYPE html>
    <html><head><title>Отчет</title></head>
    <body>
        <h1>Отчет об утечках</h1>
        <p>Найдено утечек: {len(breaches)}</p>
        <ul>
        {"".join([f"<li>{b['service_name']} ({b['breach_date']})</li>" for b in breaches])}
        </ul>
    </body></html>
    """

    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="report.html"'
    return response

# ========== VISUALIZATION ==========
@login_required
def visualize_breaches(request):
    """Визуализация с фильтрами."""
    # email может прийти из главной через ?email=...
    initial_email = request.GET.get("email", "")

    # Инициализация формы: GET-параметры + initial для email
    form = BreachFilterForm(
        request.GET or None,
        initial={"email": initial_email} if initial_email else None,
    )

    breaches = []
    if form.is_valid():
        filters = form.cleaned_data
        breaches = filter_breaches(MOCK_BREACHES, filters)

    # Данные для графика (например, количество утечек по сервисам)
    chart_labels = [b["service"] for b in breaches]
    chart_values = [1 for _ in breaches]  # можно сделать агрегацию по сервисам

    context = {
        "form": form,
        "breaches": breaches,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }
    return render(request, "leaksmap/visualize_breaches.html", context)

# ========== UTILITY FUNCTIONS ==========
def generate_checklist(breaches: List['Breach']) -> List[str]:
    """Генерация чек-листа."""
    return [
        "🔐 Смените пароли на всех сервисах",
        "✅ Включите двухфакторную аутентификацию",
        "🛡️ Проверьте аккаунты на подозрительную активность",
        "📧 Настройте мониторинг почты"
    ]

def view_feedback(request):
    """Просмотр отзывов."""
    feedbacks = []  # TODO: Feedback.objects.all()
    return render(request, 'leaksmap/view_feedback.html', {'feedbacks': feedbacks})

def generate_report(request):
    """Генерация отчета."""
    return render(request, 'leaksmap/generate_report.html')

@login_required
def create_ticket(request):
    """Создать тикет."""
    if request.method == 'POST':
        messages.success(request, 'Тикет создан!')
        return redirect('view_tickets')
    return render(request, 'leaksmap/create_ticket.html')

@login_required
def view_tickets(request):
    """Просмотр тикетов."""
    tickets = []  # TODO: Ticket.objects.filter(user=request.user)
    return render(request, 'leaksmap/view_tickets.html', {'tickets': tickets})

def view_report(request):
    """Просмотр отчета."""
    report = None  # TODO: Report.objects.get(id=report_id)
    return HttpResponse(render(request, 'leaksmap/view_report.html', {'report': report}).content)

@login_required
def edit_profile(request):
    """Редактировать профиль."""
    if request.method == 'POST':
        messages.success(request, 'Профиль обновлен!')
        return redirect('view_profile')
    profile = None  # TODO:Profile.objects.get(user=request.user)
    return render(request, 'leaksmap/edit_profile.html', {'profile': profile})

@login_required
def view_profile(request):
    """Просмотр профиля."""
    breaches_count = Breach.objects.filter(user=request.user).count()
    return render(request, 'leaksmap/profile.html', {
        'breaches_count': breaches_count
    })

def export_report(request):
    """Страница экспорта отчета."""
    return redirect('api_export_report')

MOCK_BREACHES = [
    {
        "service": "LinkedIn",
        "date": "2021-04-05",
        "location": "USA",
        "type": "passwords",
        "description": "Утечка учетных записей",
        "affected_email": "homeisdead.0@gmail.com",
    },
    {
        "service": "Adobe",
        "date": "2013-10-04",
        "location": "USA",
        "type": "emails",
        "description": "Утечка email-адресов",
        "affected_email": "homeisdead.0@gmail.com",
    },
    {
        "service": "Yahoo",
        "date": "2014-09-04",
        "location": "USA",
        "type": "passwords",
        "description": "Утечка паролей",
        "affected_email": "homeisdead.0@gmail.com",
    },
    {
        "service": "Facebook",
        "date": "2019-04-04",
        "location": "USA",
        "type": "phones",
        "description": "Утечка номеров телефонов",
        "affected_email": "homeisdead.0@gmail.com",
    },
]

def filter_breaches(all_breaches, filters_dict):
    """Фильтрация утечек по критериям."""
    filtered_breaches = all_breaches

    # Фильтр по email
    if filters_dict.get("email"):
        filtered_breaches = [b for b in filtered_breaches if b["affected_email"] == filters_dict["email"]]

    # Фильтр по типу данных
    if filters_dict.get("data_type") and filters_dict["data_type"] != "Все типы":
        filtered_breaches = [b for b in filtered_breaches if b["type"] == filters_dict["data_type"]]

    # Фильтр по дате
    if filters_dict.get("start_date"):
        filtered_breaches = [b for b in filtered_breaches if b["date"] >= filters_dict["start_date"]]
    if filters_dict.get("end_date"):
        filtered_breaches = [b for b in filtered_breaches if b["date"] <= filters_dict["end_date"]]

    return filtered_breaches
