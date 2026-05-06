from django.urls import path

from .views import PropriedadesView, PropriedadeAddView, PropriedadeUpdateView, PropriedadeDeleteView

urlpatterns = [
    path('propriedades', PropriedadesView.as_view(), name='propriedades'),
    path('propriedade/adicionar/', PropriedadeAddView.as_view(), name='propriedade_adicionar'),
    path('<int:pk>/propriedade/editar/', PropriedadeUpdateView.as_view(), name='propriedade_editar'),
    path('<int:pk>/propriedade/apagar/', PropriedadeDeleteView.as_view(), name='propriedade_apagar'),
]
