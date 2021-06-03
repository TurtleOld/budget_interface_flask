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
    days = request.form.get("days")
    months = request.form.get("months")
    years = request.form.get("years")
    get_date = f"{years}-{months}-{days}"
    print(get_date)
    number_week = request.form.get("weeks")
    print(number_week)
    weeks = ""
    error = ""
    name_seller = request.form.get("seller")
    print(name_seller)
    reseller = ""
    if name_seller == "" and number_week != "":
        cursor.execute(
            "SELECT name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) GROUP BY name_seller, date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (number_week,))
        weeks = cursor.fetchall()
    # Выводим список чеков
    elif name_seller != "":
        cursor.execute(
            "SELECT date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE name_seller=%s GROUP BY date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
            (name_seller,))
        reseller = cursor.fetchall()
    elif days and months and years:
        error = "Заполните требуемые поля"
    elif days == "" and months and years:
        error = "Не заполнено поле День"
    elif days and months == "" and years:
        error = "Не заполнено поле Месяц"
    elif days and months and years == "":
        error = "Не заполнено поле Год"
    return render_template("index.html", reseller=reseller, week=weeks, error=error)


if __name__ == '__main__':
    app.run(debug=True)
