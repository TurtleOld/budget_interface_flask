import os

from flask import Flask, render_template, request, redirect, session
from settings_database import cursor
from charts import charts_route
import logging
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from settings_database import username_bd, password_bd, host
from functions import get_full_amount_product
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, db
from wtform import LoginForm
from flask_login import LoginManager


app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

app.register_blueprint(charts_route)

load_dotenv()

logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username_bd}:{password_bd}@{host}:5432/budget"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_all():
    db.create_all()


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/accounting')
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/accounting')

    return render_template('login.html', form=form)


@app.route("/")
def default_page():
    return render_template("default.html")


@app.route("/accounting")
@login_required
def get_name_seller():
    cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller ORDER BY name_seller")
    name_sellers = cursor.fetchall()
    return render_template("index.html", name_seller=name_sellers)


@app.route("/accounting", methods=["GET", "POST"])
@login_required
def get_info():
    class DateReceipt:
        days = request.form.get("days")
        months = request.form.get("months")
        years = request.form.get("years")
        number_week = request.form.get("weeks")

    if request.method == "POST":

        days = DateReceipt.days
        months = DateReceipt.months
        years = DateReceipt.years
        number_week = DateReceipt.number_week
        name_seller = request.form.get("seller")
        get_date = f"{years}-{months}-{days}"
        data_sampling = ""
        get_amount = ""
        error = ""

        # ?????????????? ???? ???????????????? ?? ??????
        if name_seller != "" and days != "" and number_week == "" and months == "" and years == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (days, name_seller,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) and name_seller=%s GROUP BY total_sum",
                (days, name_seller,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ???????????????? ???? ???????? ????????????
        if name_seller != "" and days == "" and number_week == "" and months == "" and years == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE name_seller=%s GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (name_seller,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE name_seller=%s GROUP BY total_sum",
                (name_seller,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ???????????????? ?? ????????
        elif name_seller != "" and days == "" and number_week == "" and months == "" and years != "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) and name_seller=%s GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (years, name_seller,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) and name_seller=%s GROUP BY total_sum",
                (years, name_seller,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ???????????????? ?? ????????????
        elif name_seller != "" and days == "" and number_week == "" and months != "" and years == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (months, name_seller,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) and name_seller=%s GROUP BY total_sum",
                (months, name_seller,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ???????????????? ?? ????????????
        elif name_seller != "" and number_week != "" and days == "" and months == "" and years == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) and name_seller=%s GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (number_week, name_seller,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) and name_seller=%s GROUP BY total_sum",
                (number_week, name_seller,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ????????????
        elif name_seller == "" and number_week != "" and days == "" and months == "" and years == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (number_week,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (week from date_receipt)=%s) GROUP BY total_sum",
                (number_week,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ????????
        elif days and months and years:
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE date_receipt=%s GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (get_date,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE date_receipt=%s GROUP BY total_sum",
                (get_date,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ?????? ???????????????? ????????????
        elif name_seller == "" and days != "" and number_week == "" and months == "" and years == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (days,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (day from date_receipt)=%s) GROUP BY total_sum",
                (days,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ????????????
        elif years == "" and name_seller == "" and number_week == "" and days == "" and months != "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (months,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (month from date_receipt)=%s) GROUP BY total_sum",
                (months,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        # ?????????????? ???? ????????
        elif years != "" and name_seller == "" and number_week == "" and days == "" and months == "":
            cursor.execute(
                "SELECT date_receipt, time_receipt, name_seller, product_information, total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) GROUP BY date_receipt, time_receipt, name_seller, product_information, total_sum ORDER BY date_receipt",
                (years,))
            data_sampling = cursor.fetchall()
            cursor.execute(
                "SELECT total_sum FROM receipt WHERE (extract (year from date_receipt)=%s) GROUP BY total_sum",
                (years,))
            summation_amount = cursor.fetchall()
            get_amount = get_full_amount_product(summation_amount)

        else:
            error = "?????????????????? ?????????????????????? ????????!"
        cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller ORDER BY name_seller")
        name_sellers = cursor.fetchall()
        return render_template("index.html", data_sampling=data_sampling,
                               error=error, get_amount=get_amount, name_seller=name_sellers)


@app.route("/adding_receipt_manual", methods=["GET", "POST"])
@login_required
def adding_receipt_manual():
    return render_template("adding_receipt.html")


@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return redirect('/accounting')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
