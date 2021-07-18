from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import numpy as np
import datetime
from settings_database import cursor
from functions import get_total_amount, get_number_month

charts_route = Blueprint("charts", __name__)


# Выделяем число месяца из даты чека
def get_name_month_from_date(date_time):
    date_without_dash = date_time.replace("-", "")
    number_month = datetime.datetime.strptime(date_without_dash, "%Y%m%d").date().month
    if number_month == 1:
        return "Январь"
    elif number_month == 2:
        return "Февраль"
    elif number_month == 3:
        return "Март"
    elif number_month == 4:
        return "Апрель"
    elif number_month == 5:
        return "Май"
    elif number_month == 6:
        return "Июнь"
    elif number_month == 7:
        return "Июль"
    elif number_month == 8:
        return "Август"
    elif number_month == 9:
        return "Сентябрь"
    elif number_month == 10:
        return "Октябрь"
    elif number_month == 11:
        return "Ноябрь"
    elif number_month == 11:
        return "Декабрь"


@charts_route.route("/charts")
def charts():
    cursor.execute("SELECT * FROM receipt ORDER BY date_receipt")
    product_information = cursor.fetchall()
    listing_name_months = []
    month_listing = []
    number_month = []
    amount_total = []
    for date in product_information:
        name_month = (get_name_month_from_date(str(date[0])))
        listing_name_months.append(name_month)
        number_month.append(get_number_month(str(date[0])))
    for number in set(number_month):
        cursor.execute(
            "SELECT total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY total_sum", (number,))
        product_total_sum = cursor.fetchall()
        amount_total.append(get_total_amount(product_total_sum))
    for item in set(listing_name_months):
        month_listing.append(item)
    month_listing.sort(reverse=True)
    dict_name_months = list(set(listing_name_months))
    dict_name_months.sort(reverse=True)
    index = dict_name_months
    values = amount_total
    plt.bar(index, values)
    plt.show()
    return render_template("charts.html")

# index = [0, 1, 2, 3, 4]
# values = [5, 7, 3, 4, 6]
# plt.bar(index, values)
# plt.show()
# result = cursor.execute("SELECT total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY total_sum", (number_month,))