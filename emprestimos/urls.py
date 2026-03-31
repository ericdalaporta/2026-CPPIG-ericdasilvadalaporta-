from django.urls import path
from .views import emprestimos

app_name = 'emprestimos'

urlpatterns = [
    path('', emprestimos, name='emprestimos'),
]
