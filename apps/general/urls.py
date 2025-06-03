from django.urls import path, include
from apps.general.views import index

urlpatterns = [
    path('', index, name='index'),
]
