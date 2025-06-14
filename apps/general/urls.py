from django.urls import path, include
from apps.general.views import index, calculator_page, contact_page

urlpatterns = [
    path('', index, name='index'),
    path('calculator/', calculator_page, name='calculator_page'),
    path('contact/', contact_page, name='contact_page'),
]
