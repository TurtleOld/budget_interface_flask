from flask import Blueprint, render_template
import matplotlib.pyplot as plt
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
    if number_month == 2:
        return "Февраль"
    if number_month == 3:
        return "Март"
    if number_month == 4:
        return "Апрель"
    if number_month == 5:
        return "Май"
    if number_month == 6:
        return "Июнь"
    if number_month == 7:
        return "Июль"
    if number_month == 8:
        return "Август"
    if number_month == 9:
        return "Сентябрь"
    if number_month == 10:
        return "Октябрь"
    if number_month == 11:
        return "Ноябрь"
    if number_month == 12:
        return "Декабрь"


@charts_route.route("/charts")
def charts():
    title = "Графики"
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

    plt.title("Расходы по месяцам")
    plt.savefig("static/img/plot_monthly_expenses.png")
    return render_template("charts.html", plot_monthly_expenses="static/img/plot_monthly_expenses.png", title=title)
