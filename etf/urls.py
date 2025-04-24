from django.urls import path
from .views import etf_data_view,UserEtfView

urlpatterns = [
    path('iusq_de/getAll', etf_data_view, name='etf-iusq_de-getAll'),
    path('iusq_de', UserEtfView.as_view(), name='etf-iusq_de'),
]