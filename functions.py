import datetime


def get_full_amount_product(fetchall_item):
    list_amount = []
    for item in fetchall_item:
        conversion_to_float_amount = float(item[0])
        list_amount.append(conversion_to_float_amount)
    summation = sum(list_amount)
    return f"Сумма по выборке: {round(summation, 2)} ₽"


def get_total_amount(amount):
    list_amount = []
    for item in amount:
        conversion_to_float_amount = float(item[0])
        list_amount.append(conversion_to_float_amount)
    summation = sum(list_amount)
    return summation


def get_number_month(date_time):
    date_without_dash = date_time.replace("-", "")
    return datetime.datetime.strptime(date_without_dash, "%Y%m%d").date().month

