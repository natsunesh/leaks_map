from django.http import HttpResponseRedirect

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем /login/ и /register/, чтобы избежать бесконечного цикла редиректов
        if request.path in ['/login/', '/register/']:
            return self.get_response(request)

        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            # Редирект на /login/ с сохранением текущего пути в next
            return HttpResponseRedirect(f'/login/?next={request.path}')

        return self.get_response(request)
