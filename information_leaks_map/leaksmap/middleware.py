from django.http import HttpResponseRedirect

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("CustomAuthenticationMiddleware: __init__")

    def __call__(self, request):
        print("CustomAuthenticationMiddleware: __call__")
        # Пропускаем /login/, чтобы избежать бесконечного цикла редиректов
        if request.path == '/login/' or request.path == '/register/':
            return self.get_response(request)

        # Безопасная проверка наличия атрибута user
        if hasattr(request, 'user') and not request.user.is_authenticated:
            print(f"Redirecting to /login/?next={request.path}")
            # Редирект на /login/ с сохранением текущего пути в next
            return HttpResponseRedirect(f'/login/?next={request.path}')

        return self.get_response(request)
