# core/views.py
# This is the main landing page view for the application

from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')