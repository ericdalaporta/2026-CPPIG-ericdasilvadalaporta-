from django.urls import path
from .views import ClientesView, ClienteAddView, ClienteUpdateView, ClienteDeleteView

app_name = 'clientes'

urlpatterns = [
    path('', ClientesView.as_view(), name='list'),
    path('criar/', ClienteAddView.as_view(), name='create'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='update'),
    path('<int:pk>/deletar/', ClienteDeleteView.as_view(), name='delete'),
]
