from django.urls import path, include
from apps.general.views import index, calculator_page, contact_page, send_quote, DistanceView, partial_load

urlpatterns = [
    path('', index, name='index'),
    path('calculator/', calculator_page, name='calculator_page'),
    path('contact/', contact_page, name='contact_page'),
    path('send-quote/', send_quote, name='send_quote'),
    path('distance/', DistanceView.as_view(), name='distance_api'),
    path('partial-load/', partial_load, name='partial_load'),
]
