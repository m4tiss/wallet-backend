from rest_framework import serializers
from .models import Bond, UserBond


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'


class UserBondSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBond
        fields = ['user', 'amount', 'name', 'duration_months', 'type', 'interest_type', 'first_period_interest'
            , 'margin']
