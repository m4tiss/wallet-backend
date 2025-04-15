from django.urls import path
from .views import BondListView,UserBondListView,UserBondTotalValueView

urlpatterns = [
    path('bonds/', BondListView.as_view(), name='bond-list'),
    path('userBonds/', UserBondListView.as_view(), name='user-bond-list'),
    path('userBonds/totalValue/', UserBondTotalValueView.as_view(), name='user-bond-total-value'),
]