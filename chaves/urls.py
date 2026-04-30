from django.urls import path

from .views import (ChavesView, ChaveAddView, ChaveUpdateView, ChaveDeleteView,
                    CopiasChaveView, CopiaChaveAddView, CopiaChaveUpdateView, CopiaChaveDeleteView)

urlpatterns = [
    path('chaves', ChavesView.as_view(), name='chaves'),
    path('chave/adicionar/', ChaveAddView.as_view(), name='chave_adicionar'),
    path('<int:pk>/chave/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/chave/apagar/', ChaveDeleteView.as_view(), name='chave_apagar'),
    
    path('copias', CopiasChaveView.as_view(), name='copias'),
    path('copia/adicionar/', CopiaChaveAddView.as_view(), name='copia_adicionar'),
    path('<int:pk>/copia/editar/', CopiaChaveUpdateView.as_view(), name='copia_editar'),
    path('<int:pk>/copia/apagar/', CopiaChaveDeleteView.as_view(), name='copia_apagar'),
]
