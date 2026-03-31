from django.urls import path
from .views import propriedades

app_name = 'propriedades'

urlpatterns = [
    path('', propriedades, name='propriedades'),
]
