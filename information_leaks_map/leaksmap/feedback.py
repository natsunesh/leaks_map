from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Feedback

def submit_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        Feedback.objects.create(user=request.user, content=feedback)
        return JsonResponse({'message': 'Feedback submitted successfully'})
    return render(request, 'leaksmap/feedback.html')

def view_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'leaksmap/view_feedback.html', {'feedbacks': feedbacks})
