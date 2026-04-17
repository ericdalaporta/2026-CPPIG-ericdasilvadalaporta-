from django.urls import path
from .views import index, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]