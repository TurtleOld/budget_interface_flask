from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import numpy as np
from settings_database import cursor

charts_route = Blueprint("charts", __name__)


@charts_route.route("/charts")
def charts():
    fig1, ax1 = plt.subplots()
    cursor.execute("SELECT name_product, amount FROM receipt GROUP BY name_product, amount")
    product_amount = cursor.fetchall()
    product = []
    amount = []
    for item in product_amount:
        product.append(item[0])
        amount.append(item[1])
    names = product
    values = amount
    ax1.pie(values, labels=names)
    plt.show()
    return render_template("charts.html")

