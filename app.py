from flask import Flask, render_template, request
from settings_database import cursor
import logging

app = Flask(__name__)

logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG)


@app.route("/")
def default_page():
    return render_template("default.html")


@app.route("/accounting")
def get_name_seller():
    cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller")
    name_sellers = cursor.fetchall()
    return render_template("index.html", name_seller=name_sellers)


@app.route("/accounting", methods=["GET", "POST"])
def get_info():
    def get_amount_product(fetchall_item):
        list_amount = []
        for item in fetchall_item:
            list_amount.append(item[1])
        summation = sum(list_amount)
        return f"Сумма по выборке: {round(summation, 2)} ₽"

    days = request.form.get("days")
    months = request.form.get("months")
    years = request.form.get("years")
    get_receipt_for_date = ""
    get_date = f"{years}-{months}-{days}"
    number_week = request.form.get("weeks")
    weeks = ""
    set_years = ""
    set_months = ""
    error = ""
    name_seller = request.form.get("seller")
    reseller = ""
    get_current_month_day = ""
    get_info_for_current_month = ""
    get_amount = ""

    # Выборка по продавцу и дню
    if name_seller != "" and days != "" and number_week == "" and months == "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (days, name_seller,))
        get_current_month_day = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s GROUP BY name_product, amount",
            (days, name_seller,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по продавцу за весь период
    elif name_seller != "" and days == "" and number_week == "" and months == "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (name_seller,))
        reseller = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE name_seller=%s GROUP BY name_product, amount",
            (name_seller,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по продавцу и году
    elif name_seller != "" and days == "" and number_week == "" and months == "" and years != "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) and name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (years, name_seller,))
        get_current_month_day = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (year from date_receipt)=%s) and name_seller=%s GROUP BY name_product, amount",
            (years, name_seller,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по продавцу и месяцу
    elif name_seller != "" and days == "" and number_week == "" and months != "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (months, name_seller,))
        get_info_for_current_month = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s GROUP BY name_product, amount",
            (months, name_seller,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по продавцу и неделе
    elif name_seller != "" and number_week != "" and days == "" and months == "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) and name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (number_week, name_seller,))
        weeks = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (week from date_receipt)=%s) and name_seller=%s GROUP BY name_product, amount",
            (number_week, name_seller,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по неделе
    elif name_seller == "" and number_week != "" and days == "" and months == "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (number_week,))
        weeks = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (week from date_receipt)=%s) GROUP BY name_product, amount",
            (number_week,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по дате
    elif days and months and years:
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE date_receipt=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (get_date,))
        get_receipt_for_date = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE date_receipt=%s GROUP BY name_product, amount",
            (get_date,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по дню текущего месяца
    elif name_seller == "" and days != "" and number_week == "" and months == "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (days,))
        get_current_month_day = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (day from date_receipt)=%s) GROUP BY name_product, amount",
            (days,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по месяцу
    elif years == "" and name_seller == "" and number_week == "" and days == "" and months != "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (months,))
        set_months = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY name_product, amount",
            (months,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    # Выборка по году
    elif years != "" and name_seller == "" and number_week == "" and days == "" and months == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (years,))
        set_years = cursor.fetchall()
        cursor.execute(
            "SELECT name_product, amount FROM receipt WHERE (extract (year from date_receipt)=%s) GROUP BY name_product, amount",
            (years,))
        summation_amount = cursor.fetchall()
        get_amount = get_amount_product(summation_amount)

    elif days == "" and months and years:
        error = "Не заполнено поле День"
    elif days and months == "" and years:
        error = "Не заполнено поле Месяц"
    elif days and months and years == "":
        error = "Не заполнено поле Год"
    else:
        error = "Заполните необходимые поля!"
    return render_template("index.html", reseller=reseller, week=weeks, get_receipt_for_date=get_receipt_for_date,
                           set_years=set_years, set_months=set_months, get_current_month_day=get_current_month_day,
                           get_info_for_current_month=get_info_for_current_month,
                           error=error, get_amount=get_amount)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
