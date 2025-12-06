from typing import List
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
import asyncio
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.utils import timezone
import os
from .api_client import LeakCheckAPIClient
from .models import Breach  # Только существующие модели
from .forms import (
    RegistrationForm, LoginForm, CheckBreachesForm, ExportReportForm
)  # Только существующие формы
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
def home_view(request):
    """Главная страница."""
    context = {
        'check_form': CheckBreachesForm(),
        'export_form': ExportReportForm(),
    }
    return render(request, 'leaksmap/home.html', context)

# ========== API ENDPOINTS ==========
@login_required
@require_http_methods(["POST"])
def api_check_leaks(request):
    """AJAX проверка утечек (исправлена async проблема)."""
    form = CheckBreachesForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": dict(form.errors)}, status=400)

    email = form.cleaned_data['email']
    api_key = os.getenv('LEAKCHECK_API_KEY')

    if not api_key:
        return JsonResponse({"error": "API ключ не настроен"}, status=500)

    try:
        client = LeakCheckAPIClient(api_key)
        # FIXED: Правильный вызов async метода
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        breaches_data = loop.run_until_complete(client.get_breach_info_by_email(email))
        loop.close()

        if not breaches_data:
            return JsonResponse({
                "status": "success",
                "count": 0,
                "message": "Утечки не найдены",
                "checklist": generate_checklist([]),
                "advice": generate_security_advice([])
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
            "checklist": generate_checklist(saved_breaches),
            "advice": generate_security_advice(saved_breaches),
        })

    except Exception as e:
        logger.error(f"API error: {e}")
        return JsonResponse({"error": "Ошибка проверки API"}, status=500)

@login_required
@require_http_methods(["POST"])
def api_export_report(request):
    """AJAX экспорт отчета (убрано render_to_string)."""
    form = ExportReportForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": dict(form.errors)}, status=400)

    format_type = form.cleaned_data['format']
    breaches = list(Breach.objects.filter(user=request.user).values(
        'service_name', 'breach_date', 'data_type', 'description'
    )[:50])

    # Простой HTML без render_to_string
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
    breaches = Breach.objects.filter(user=request.user).order_by('-breach_date')

    # Фильтры
    email_filter = request.GET.get('email')
    data_type = request.GET.get('data_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if email_filter:
        breaches = breaches.filter(user__email__icontains=email_filter)
    if data_type:
        breaches = breaches.filter(data_type=data_type)
    if start_date:
        breaches = breaches.filter(breach_date__gte=start_date)
    if end_date:
        breaches = breaches.filter(breach_date__lte=end_date)

    # Подсчет для фильтров
    results_count = breaches.count()

    # Chart.js данные для визуализации
    services = breaches.values('service_name').annotate(count=Count('id')).order_by('-count')
    chart_data = {
        'labels': [s['service_name'][:15] for s in services],
        'data': [s['count'] for s in services]
    }

    context = {
        'current_filters': {
            'email': email_filter,
            'data_type': data_type,
            'start_date': start_date,
            'end_date': end_date,
        },
        'data_types': list(Breach.objects.filter(user=request.user)
                          .values_list('data_type', flat=True).distinct()),
        'results_count': results_count,
        'chart_data': chart_data,
        'breaches': breaches[:20]  # Первые 20 для превью
    }
    return render(request, 'leaksmap/visualize_breaches.html', context)

# ========== UTILITY FUNCTIONS ==========
def generate_checklist(breaches: List['Breach']) -> List[str]:
    """Генерация чек-листа."""
    return [
        "🔐 Смените пароли на всех сервисах",
        "✅ Включите двухфакторную аутентификацию",
        "🛡️ Проверьте аккаунты на подозрительную активность",
        "📧 Настройте мониторинг почты"
    ]

def generate_security_advice(breaches: List['Breach']) -> str:
    """Генерация рекомендаций."""
    if not breaches:
        return "✅ Email чист! Продолжайте соблюдать безопасность."

    advice = "🚨 Срочно выполните:\n\n"
    services = {b.service_name for b in breaches[:5]}
    for service in services:
        advice += f"• {service}: смените пароль\n"
    advice += "\n📋 Общие меры:\n• Уникальные пароли\n• 2FA везде\n• Менеджер паролей"
    return advice
