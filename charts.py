from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import numpy as np

charts_route = Blueprint("charts", __name__)


@charts_route.route("/charts")
def charts():
    fig1, ax1 = plt.subplots()
    names = ["One", "Two", "Three"]
    values = [55, 102, 100]
    ax1.pie(values, labels=names)
    plt.show()
    return render_template("charts.html")

