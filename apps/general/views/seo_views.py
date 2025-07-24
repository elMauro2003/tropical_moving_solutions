from django.shortcuts import render

def robots(request):
    return render(request, "txts/robots.txt", context={"domain_url": "http://localhost:8000"}, content_type="text/plain")

def security(request):
    return render(request, "txts/security.txt", content_type="text/plain")

def humans(request):
    return render(request, "txts/humans.txt", content_type="text/plain")