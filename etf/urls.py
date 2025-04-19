from django.urls import path
from .views import etf_data_view,UserEtfView

urlpatterns = [
    path('iusq_de', etf_data_view, name='etf-iusq_de'),
    path('iusq_de/add', UserEtfView.as_view(), name='etf-iusq_de-add'),
]