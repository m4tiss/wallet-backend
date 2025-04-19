from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.utils import get_user_id
from .models import UserEtf

from .scraper import get_iusq_de
from .serializers import UserEtfSerializer


@api_view(['GET'])
def etf_data_view(request):
    try:
        exchange, date, time, daily_change_value, daily_change_percent, bid, ask = get_iusq_de()
        return Response({
            "exchange": exchange,
            "date": date,
            "time": time,
            "daily_change_value": daily_change_value,
            "daily_change_percent": daily_change_percent,
            "bid": bid,
            "ask": ask
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


class UserEtfView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = get_user_id(request)
            name = request.data.get('name')
            purchase_date = request.data.get('purchase_date')
            purchase_price = request.data.get('purchase_price')
            units = request.data.get('units')

            user_etf = UserEtf.objects.create(
                user_id=user_id,
                name=name,
                purchase_date=purchase_date,
                purchase_price=purchase_price,
                units=units
            )

            serializer = UserEtfSerializer(user_etf)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
