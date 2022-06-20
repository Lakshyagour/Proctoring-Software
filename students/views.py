from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'students/dashboard.html')


def give_test(request):
    return render(request, 'students/give-test.html')


def exam_history(request):
    return render(request, 'students/dashboard.html')
