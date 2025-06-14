from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'base.html')

def calculator_page(request):
    return render(request, 'calculator.html')

def contact_page(request):
    return render(request, 'contact.html')