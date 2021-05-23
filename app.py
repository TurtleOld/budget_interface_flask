from flask import Flask, render_template, request
from settings_database import cursor

app = Flask(__name__)


@app.route('/')
def get_name_seller():
    cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller")
    name_sellers = cursor.fetchall()
    return render_template("index.html", name=name_sellers)


@app.route('/', methods=["GET", "POST"])
def get_info():
    name_seller = request.form.get("seller")
    year = request.form.get("years")
    if name_seller is not None:
        cursor.execute(
            "SELECT date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE "
            "name_seller=%s ORDER BY date_receipt",
            (name_seller,))
        reseller = cursor.fetchall()
        return render_template("index.html", reseller=reseller)
    if year is not None:
        cursor.execute()


if __name__ == '__main__':
    app.run(debug=True)
