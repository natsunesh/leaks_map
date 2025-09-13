from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Recommendation

@login_required
def recommendations(request):
    recommendations = Recommendation.objects.filter(user=request.user)
    return render(request, 'leaksmap/recommendations.html', {'recommendations': recommendations})

def get_security_advice():
    return "Use strong, unique passwords for all your accounts. Enable two-factor authentication where possible."

def generate_checklist(email):
    return [
        "Change your password immediately.",
        "Enable two-factor authentication.",
        "Monitor your accounts for unusual activity.",
        "Consider using a password manager."
    ]
