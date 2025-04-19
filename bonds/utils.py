import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from dateutil.relativedelta import relativedelta


def check_duration(bond):
    end_date = bond.purchase_date + relativedelta(months=bond.duration_months)
    today = datetime.now().date()

    if today > end_date and bond.is_active:
        bond.is_active = False
        bond.save()


def get_dict():
    inflation_data = {}
    current_dir = os.path.dirname(__file__)
    inflation_file_path = os.path.join(current_dir, "InflationData.txt")

    with open(inflation_file_path, "r") as file:
        for line in file:
            if line.strip():
                key, value = line.strip().split()
                inflation_data[key] = value

    return inflation_data


def get_date_data(bond):
    purchase_date = datetime.combine(bond.purchase_date, datetime.min.time())
    end_date = purchase_date + relativedelta(months=bond.duration_months)
    today = datetime.today()
    total_days = (end_date - purchase_date).days
    elapsed_days = (today - purchase_date).days
    percent_progress = (elapsed_days / total_days) * 100 if total_days > 0 else 0
    return end_date.date(), percent_progress


def calculate_generated_money(bond):
    purchase_date = bond.purchase_date
    today = datetime.now().date()
    obligation_value = Decimal("100")
    amount = bond.amount * obligation_value
    total_generated = Decimal("0.00")
    days_passed = (today - purchase_date).days

    if bond.interest_type == "fixed":
        interest = Decimal(bond.first_period_interest) / Decimal("100")
        daily_interest_rate = interest / Decimal("365")
        daily_interest = (amount * daily_interest_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_generated = daily_interest * days_passed

    elif bond.interest_type == "variable":
        first_year_days = 365 if days_passed > 365 else days_passed
        interest = Decimal(bond.first_period_interest) / Decimal("100")
        daily_interest_rate = interest / Decimal("365")
        daily_interest = (amount * daily_interest_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_generated = daily_interest * first_year_days
        if days_passed > 365:
            remaining_days = days_passed - 365
            adjusted_interest_rate = interest + bond.margin / 100
            adjusted_daily_interest_rate = adjusted_interest_rate / Decimal("365")
            adjusted_daily_interest = (amount * adjusted_daily_interest_rate).quantize(Decimal("0.01"),
                                                                                       rounding=ROUND_HALF_UP)
            total_generated += adjusted_daily_interest * remaining_days

    elif bond.interest_type == 'indexed':
        inflation_data = get_dict()
        margin = Decimal(bond.margin) / Decimal("100")
        first_year_days = min(days_passed, 365)
        fixed_interest = Decimal(bond.first_period_interest) / Decimal("100")
        daily_interest_rate = fixed_interest / Decimal("365")
        daily_interest = (amount * daily_interest_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        yearly_interest = daily_interest * first_year_days
        total_generated += yearly_interest
        cumulative_amount = amount + yearly_interest

        print(
            f"1. rok: Stałe oprocentowanie = {fixed_interest * 100}%, Dni: {first_year_days}, Odsetki: {yearly_interest} zł")

        if days_passed > 365:
            remaining_days = days_passed - 365
            current_date = purchase_date + relativedelta(years=1)
            days_to_process = remaining_days

            while days_to_process > 0:
                days_this_year = min(365, days_to_process)
                inflation_month = (current_date - relativedelta(months=2)).strftime("%Y.%m")
                inflation_rate = Decimal(inflation_data.get(inflation_month, 0)) / Decimal("100")
                adjusted_interest_rate = inflation_rate + margin
                daily_rate = adjusted_interest_rate / Decimal("365")
                daily_interest = (cumulative_amount * daily_rate).quantize(Decimal("0.01"),
                                                                           rounding=ROUND_HALF_UP)
                yearly_interest = daily_interest * days_this_year
                total_generated += yearly_interest
                cumulative_amount += yearly_interest

                print(

                    f"{current_date.year}: Inflacja ({inflation_month}) = {inflation_rate * 100}%, Marża = {margin * 100}%, Dni: {days_this_year}, Odsetki: {yearly_interest} zł, Skumulowana kwota: {cumulative_amount} zł"

                )

                current_date += relativedelta(years=1)
                days_to_process -= days_this_year

    return total_generated
