from django.urls import path

from .views import PropriedadesView, PropriedadeAddView, PropriedadeUpdateView, PropriedadeDeleteView, PropriedadeToggleStatusView

urlpatterns = [
    path('propriedades', PropriedadesView.as_view(), name='propriedades'),
    path('propriedade/adicionar/', PropriedadeAddView.as_view(), name='propriedade_adicionar'),
    path('<int:pk>/propriedade/editar/', PropriedadeUpdateView.as_view(), name='propriedade_editar'),
    path('<int:pk>/propriedade/apagar/', PropriedadeDeleteView.as_view(), name='propriedade_apagar'),
    path('<int:pk>/propriedade/toggle-status/', PropriedadeToggleStatusView.as_view(), name='propriedade_toggle_status'),
]
