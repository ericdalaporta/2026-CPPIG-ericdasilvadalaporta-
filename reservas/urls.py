from django.urls import path
from .views import reservas

app_name = 'reservas'

urlpatterns = [
    path('', reservas, name='reservas'),
]
