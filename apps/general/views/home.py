from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'base.html')

def calculator_page(request, plan_type=None):
    context = {}
    if plan_type is not None:
        context = {'plan_type': plan_type}
    return render(request, 'calculator/calculator.html', context)

def contact_page(request):
    return render(request, 'contact/contact.html')

        

