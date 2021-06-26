from flask import Flask, render_template, request, url_for
from settings_database import cursor
from charts import charts_route
import logging


app = Flask(__name__)
app.register_blueprint(charts_route)

logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG)


@app.route("/")
def default_page():
    return render_template("default.html")


@app.route("/accounting")
def get_name_seller():
    cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller ORDER BY name_seller")
    name_sellers = cursor.fetchall()
    return render_template("index.html", name_seller=name_sellers)


@app.route("/accounting", methods=["GET", "POST"])
def get_info():
    if request.method == "POST":
        def get_full_amount_product(fetchall_item):
            list_amount = []
            for item in fetchall_item:
                conversion_to_float_amount = float(item[1])
                list_amount.append(conversion_to_float_amount)
            summation = sum(list_amount)
            return f"Сумма по выборке: {round(summation, 2)} ₽"

        days = request.form.get("days")
        months = request.form.get("months")
        years = request.form.get("years")
        number_week = request.form.get("weeks")
        name_seller = request.form.get("seller")
        get_date = f"{years}-{months}-{days}"
        name_seller_receipt = ""
        date_receipt = ""
        time_receipt = ""
        result_receipt = ""
        data_sampling = ""
        get_amount = ""
        error = ""

        # Выборка по продавцу и дню
        # if name_seller != "" and days != "" and number_week == "" and months == "" and years == "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s ORDER BY date_receipt",
        #         (days, name_seller,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s",
        #         (days, name_seller,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)

        # Выборка по продавцу за весь период
        if name_seller != "" and days == "" and number_week == "" and months == "" and years == "":
            cursor.execute(
                "SELECT * FROM receipt WHERE name_seller=%s ORDER BY date_receipt",
                (name_seller,))
            data_sampling = cursor.fetchall()
            for item in data_sampling:
                name_seller_receipt = item[2]
                date_receipt = item[0]
                time_receipt = item[1]
                result_receipt = item[4]
            cursor.execute(
                "SELECT product_information[1], product_information[4] FROM receipt WHERE name_seller=%s GROUP BY product_information[1], product_information[4]",
                (name_seller,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по продавцу и году
        # elif name_seller != "" and days == "" and number_week == "" and months == "" and years != "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (year from date_receipt)=%s) and name_seller=%s ORDER BY date_receipt",
        #         (years, name_seller,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (year from date_receipt)=%s) and name_seller=%s",
        #         (years, name_seller,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по продавцу и месяцу
        # elif name_seller != "" and days == "" and number_week == "" and months != "" and years == "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s ORDER BY date_receipt",
        #         (months, name_seller,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s",
        #         (months, name_seller,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по продавцу и неделе
        # elif name_seller != "" and number_week != "" and days == "" and months == "" and years == "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (week from date_receipt)=%s) and name_seller=%s ORDER BY date_receipt",
        #         (number_week, name_seller,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (week from date_receipt)=%s) and name_seller=%s",
        #         (number_week, name_seller,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по неделе
        # elif name_seller == "" and number_week != "" and days == "" and months == "" and years == "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (week from date_receipt)=%s) ORDER BY date_receipt",
        #         (number_week,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (week from date_receipt)=%s)",
        #         (number_week,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по дате
        # elif days and months and years:
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE date_receipt=%s ORDER BY date_receipt",
        #         (get_date,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE date_receipt=%s",
        #         (get_date,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по дню текущего месяца
        # elif name_seller == "" and days != "" and number_week == "" and months == "" and years == "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (day from date_receipt)=%s) ORDER BY date_receipt",
        #         (days,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (day from date_receipt)=%s)",
        #         (days,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по месяцу
        # elif years == "" and name_seller == "" and number_week == "" and days == "" and months != "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (month from date_receipt)=%s) ORDER BY date_receipt",
        #         (months,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (month from date_receipt)=%s)",
        #         (months,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        # # Выборка по году
        # elif years != "" and name_seller == "" and number_week == "" and days == "" and months == "":
        #     cursor.execute(
        #         "SELECT * FROM receipt WHERE (extract (year from date_receipt)=%s) ORDER BY date_receipt",
        #         (years,))
        #     data_sampling = cursor.fetchall()
        #     cursor.execute(
        #         "SELECT name_product, amount FROM receipt WHERE (extract (year from date_receipt)=%s)",
        #         (years,))
        #     summation_amount = cursor.fetchall()
        #     get_amount = get_full_amount_product(summation_amount)
        #
        #
        #
        # elif days == "" and months and years:
        #     error = "Не заполнено поле День"
        # elif days and months == "" and years:
        #     error = "Не заполнено поле Месяц"
        # elif days and months and years == "":
        #     error = "Не заполнено поле Год"
        # else:
        #     error = "Заполните необходимые поля!"
        cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller ORDER BY name_seller")
        name_sellers = cursor.fetchall()
        return render_template("index.html", data_sampling=data_sampling,
                               error=error, get_amount=get_amount, name_seller=name_sellers,
                               name_seller_receipt=name_seller_receipt, date_receipt=date_receipt,
                               time_receipt=time_receipt, result_receipt=result_receipt)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
