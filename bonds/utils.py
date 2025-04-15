from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from dateutil.relativedelta import relativedelta


def check_duration(bond):
    end_date = bond.purchase_date + relativedelta(months=bond.duration_months)
    today = datetime.now().date()

    if today > end_date and bond.is_active:
        bond.is_active = False
        bond.save()


def calculate_generated_money(bond):
    purchase_date = bond.purchase_date
    today = datetime.now().date()
    days_since_purchase = (today - purchase_date).days

    obligation_value = Decimal("100")
    interest = Decimal(bond.first_period_interest) / Decimal(100)

    days_decimal = Decimal(days_since_purchase) / Decimal(365)
    amount = bond.amount * obligation_value
    if bond.interest_type == "fixed":
        generated_money = (amount * interest * days_decimal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        generated_money = 0
    return generated_money
