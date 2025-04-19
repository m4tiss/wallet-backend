from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scraper import get_iusq_de


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
