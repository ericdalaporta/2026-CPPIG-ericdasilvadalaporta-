from django.urls import path
from .views import registros

app_name = 'registros'

urlpatterns = [
    path('', registros, name='registros'),
]
