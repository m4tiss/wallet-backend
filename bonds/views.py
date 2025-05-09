from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.utils import get_user_id
from .models import Bond, UserBond
from .serializers import BondSerializer, UserBondSerializer
from .utils import calculate_generated_money, check_duration, get_date_data


class BondListView(APIView):
    def get(self, request):
        bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)


class UserBondListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = get_user_id(request)
            user_bonds = UserBond.objects.filter(user_id=user_id)

            bond_data = []

            for bond in user_bonds:
                check_duration(bond)

                if not bond.is_active:
                    continue

                generated_money = calculate_generated_money(bond)
                end_date, percent_progress = get_date_data(bond)

                bond_info = {
                    'id': bond.id,
                    'amount': bond.amount,
                    'start_date': bond.purchase_date,
                    'end_date': end_date,
                    'percent_progress': percent_progress,
                    'generated_money': generated_money,
                    'name': bond.name,
                    'duration_months': bond.duration_months,
                    'interest_type': bond.interest_type,
                    'first_period_interest': bond.first_period_interest,
                    'margin': bond.margin,
                }

                bond_data.append(bond_info)

            serializer = Response(bond_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            user_id = get_user_id(request)
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


class UserBondTotalValueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = get_user_id(request)
            user_bonds = UserBond.objects.filter(user_id=user_id)

            start_money = 0
            total_value = 0

            for bond in user_bonds:
                check_duration(bond)

                if not bond.is_active:
                    continue

                generated = calculate_generated_money(bond)
                start_money += (bond.amount * 100)
                total_value += (bond.amount* 100) + generated

            percent = ((total_value - start_money) / start_money * 100) if start_money else 0

            return Response({
                "start_money": round(start_money, 2),
                "total_value": round(total_value, 2),
                "percent": round(percent, 2),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)