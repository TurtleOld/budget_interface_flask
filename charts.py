from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import numpy as np
import datetime
from settings_database import cursor
from functions import get_total_amount

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
    # print(product_information)
    # print(get_name_month_from_date(str(product_amount[0][0])))
    listing_month = []
    month_listing = []
    for date in product_information:
        result = (get_name_month_from_date(str(date[0])))
        listing_month.append(result)
    for item in set(listing_month):
        month_listing.append(item)
    month_listing.sort(reverse=True)

    cursor.execute("SELECT total_sum FROM receipt WHERE (extract (month from date_receipt)=5) GROUP BY total_sum")
    product_total_sum = cursor.fetchall()
    print(get_total_amount(product_total_sum))

    return render_template("charts.html")

# index = [0, 1, 2, 3, 4]
# values = [5, 7, 3, 4, 6]
# plt.bar(index, values)
# plt.show()
