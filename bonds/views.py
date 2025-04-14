from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken

from .models import Bond, UserBond
from .serializers import BondSerializer,UserBondSerializer


class BondListView(APIView):
    def get(self, request):
        bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)


class UserBondListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            untokened = UntypedToken(token)
            user_id = untokened.payload['user_id']
            user_bonds = UserBond.objects.filter(user_id=user_id)
            serializer = UserBondSerializer(user_bonds, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            untokened = UntypedToken(token)
            user_id = untokened.payload['user_id']
            amount = request.data.get('amount')
            name = request.data.get('name')
            duration_months = request.data.get('duration_months')
            type = request.data.get('type')
            interest_type = request.data.get('interest_type')
            first_period_interest = request.data.get('first_period_interest')
            margin = request.data.get('margin')

            user_bond = UserBond.objects.create(
                user_id=user_id,
                amount=amount,
                name=name,
                duration_months=duration_months,
                type=type,
                interest_type=interest_type,
                first_period_interest=first_period_interest,
                margin=margin
            )

            serializer = UserBondSerializer(user_bond)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)