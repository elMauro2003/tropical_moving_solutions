from django.urls import path, include
#from apps.general.views import index, calculator_page, contact_page, send_quote, DistanceView, partial_load
from apps.general.views import *

urlpatterns = [
    path('', index, name='index'),
    path('calculator/', calculator_page, name='calculator_page'),
    path('contact/', contact_page, name='contact_page'),
    path('send-quote/', send_quote, name='send_quote'),
    path('distance/', DistanceView.as_view(), name='distance_api'),
    path('partial-load/', partial_load, name='partial_load'),
    path('send-mail/', send_mail, name='send_mail'),
    path('send-mail-quote/', send_mail_quote, name='send_mail_quote'),
]
