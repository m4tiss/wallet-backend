from rest_framework import serializers
from .models import UserEtf


class UserEtfSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEtf
        fields = ['user', 'name', 'purchase_date', 'purchase_price', 'units']
