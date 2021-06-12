from flask import Blueprint, render_template

charts_route = Blueprint("charts", __name__)


@charts_route.route("/charts")
def charts():
    test = "Проверка"
    return render_template("charts.html", test=test)

