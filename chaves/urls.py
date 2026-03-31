from django.urls import path
from .views import chaves

app_name = 'chaves'

urlpatterns = [
    path('', chaves, name='chaves'),
]
