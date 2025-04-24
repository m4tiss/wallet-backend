from .scraper import get_iusq_de
import requests
from decimal import Decimal


def get_bid_exchange_rate():
    url = "https://api.nbp.pl/api/exchangerates/rates/c/eur"
    response = requests.get(url)
    response.raise_for_status()
    # mozna uzyc lepszego kursu ale jest ok
    data = response.json()
    bid = data['rates'][0]['bid']
    return Decimal(str(bid))

def calculate_generated_money(etf):
    try:
        bid, ask = get_iusq_de()

        current_price = Decimal(str(bid))
        current_euro_exchange_rate = get_bid_exchange_rate()
        current_value = current_price * etf.units * current_euro_exchange_rate
        initial_value = etf.purchase_price * etf.units * etf.euro_exchange_rate
        percent_change = ((current_value - initial_value) / initial_value) * Decimal('100')

        return round(current_value, 4), round(initial_value, 4), round(percent_change, 4)
    except Exception as e:
        print(f"Error calculating generated money: {e}")
        return 0, 0, 0
