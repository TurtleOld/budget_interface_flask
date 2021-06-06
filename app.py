from flask import Flask, render_template, request
from settings_database import cursor

app = Flask(__name__)


@app.route("/")
def get_name_seller():
    cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller")
    name_sellers = cursor.fetchall()
    return render_template("index.html", name_seller=name_sellers)


@app.route("/", methods=["GET", "POST"])
def get_info():
    def get_amount_product(fetchall_item):
        for item in fetchall_item:
            return f"Сумма по выборке: {round(item[0], 2)} ₽"

    days = request.form.get("days")
    print(days)
    months = request.form.get("months")
    print(months)
    years = request.form.get("years")
    print(years)
    get_receipt_for_date = ""
    get_date = f"{years}-{months}-{days}"
    print(get_date)
    number_week = request.form.get("weeks")
    weeks = ""
    set_years = ""
    set_months = ""
    error = ""
    name_seller = request.form.get("seller")
    print(name_seller)
    reseller = ""
    get_current_month_day = ""
    get_info_for_current_month = ""
    sum_price = ""
    get_amount = ""

    if name_seller != "" and days != "" and number_week == "" and months == "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (days, name_seller,))
        get_current_month_day = cursor.fetchall()

    if name_seller != "" and days == "" and number_week == "" and months != "" and years == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (months, name_seller,))
        get_info_for_current_month = cursor.fetchall()
        cursor.execute(
            "SELECT sum(amount) FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s",
            (months, name_seller,))
        sum_price = cursor.fetchall()
        get_amount = get_amount_product(sum_price)

    elif name_seller != "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE name_seller=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (name_seller,))
        reseller = cursor.fetchall()

    elif name_seller == "" and number_week != "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (number_week,))
        weeks = cursor.fetchall()

    elif days and months and years:
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE date_receipt=%s GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (get_date,))
        get_receipt_for_date = cursor.fetchall()

    elif years == "" and name_seller == "" and number_week == "" and days == "" and months != "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (months,))
        set_months = cursor.fetchall()

    elif years != "" and name_seller == "" and number_week == "" and days == "" and months == "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (years,))
        set_years = cursor.fetchall()

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
