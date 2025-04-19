from django.urls import path
from .views import etf_data_view

urlpatterns = [
    path('iusq_de', etf_data_view, name='etf-iusq_de'),
]