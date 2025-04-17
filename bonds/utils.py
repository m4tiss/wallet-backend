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


def calculate_generated_money(bond):
    purchase_date = bond.purchase_date
    today = datetime.now().date()
    obligation_value = Decimal("100")
    amount = bond.amount * obligation_value
    total_generated = Decimal("0.00")

    days_passed = (today - purchase_date).days
    print(f"\nData zakupu obligacji: {purchase_date}")
    print(f"Data dzisiejsza: {today}")
    print(f"Liczba dni od zakupu: {days_passed}")
    print(f"Kwota obligacji: {amount}")

    if bond.interest_type == "fixed":
        interest = Decimal(bond.first_period_interest) / Decimal("100")
        daily_interest_rate = interest / Decimal("365")
        daily_interest = (amount * daily_interest_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_generated = daily_interest * days_passed

    elif bond.interest_type == "variable":
        print("Rodzaj oprocentowania: Zmiennoprocentowe")
        # Zmiennoprocentowe – pierwszy miesiąc stały, reszta inflacja + marża
        inflation_data = get_dict()
        margin = Decimal(bond.margin) / Decimal("100")
        print(f"Marża: {margin * 100}%")

        for i in range(days_passed):
            period_date = purchase_date + relativedelta(days=i)
            key = period_date.strftime("%Y.%m")

            if i == 0:
                interest = Decimal(bond.first_period_interest) / Decimal("100")
                print(f"Pierwszy dzień - oprocentowanie: {interest * 100}%")
            else:
                inflation = Decimal(inflation_data.get(key, "0")) / Decimal("100")
                interest = margin + inflation
                print(f"Okres {period_date.strftime('%Y-%m')}: Oprocentowanie inflacyjne: {interest * 100}% (marża + inflacja)")

            daily_interest = (amount * interest / Decimal("365")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            print(f"Odsetki dzienne dla dnia {i + 1}: {daily_interest}")
            total_generated += daily_interest
            print(f"Całkowity wygenerowany zysk po dniu {i + 1}: {total_generated}")

    return total_generated