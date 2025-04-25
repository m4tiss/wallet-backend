from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.utils import get_user_id
from .models import UserEtf
from .utils import calculate_generated_money
from .scraper import get_iusq_de
from .serializers import UserEtfSerializer


@api_view(['GET'])
def etf_data_view(request):
    try:
        bid, ask = get_iusq_de()
        return Response({
            "bid": bid,
            "ask": ask
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


class UserEtfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = get_user_id(request)
            user_etf = UserEtf.objects.filter(user_id=user_id)

            etf_data = []

            bid, ask = get_iusq_de()
            for etf in user_etf:
                current_value, initial_value, percent_change = calculate_generated_money(etf, bid)
                etf_info = {
                    'id': etf.id,
                    'name': etf.name,
                    'purchase_date': etf.purchase_date,
                    'purchase_price': etf.purchase_price,
                    'units': etf.units,
                    'current_value': current_value,
                    'initial_value': initial_value,
                    'percent_change': percent_change
                }
                etf_data.append(etf_info)

            return Response(etf_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            user_id = get_user_id(request)
            name = request.data.get('name')
            purchase_date = request.data.get('purchase_date')
            purchase_price = request.data.get('purchase_price')
            units = request.data.get('units')
            euro_exchange_rate = request.data.get('euro_exchange_rate')

            user_etf = UserEtf.objects.create(
                user_id=user_id,
                name=name,
                purchase_date=purchase_date,
                purchase_price=purchase_price,
                units=units,
                euro_exchange_rate=euro_exchange_rate
            )

            serializer = UserEtfSerializer(user_etf)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserEtfTotalValueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = get_user_id(request)
            user_etf = UserEtf.objects.filter(user_id=user_id)

            start_money = 0
            total_value = 0

            bid, ask = get_iusq_de()
            for etf in user_etf:
                current_value, initial_value, percent_change = calculate_generated_money(etf, bid)
                start_money += initial_value;
                total_value += current_value

            percent = ((total_value - start_money) / start_money * 100) if start_money else 0

            return Response({
                "start_money": round(start_money, 2),
                "total_value": round(total_value, 2),
                "percent": round(percent, 2),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
