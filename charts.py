from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import numpy as np

charts_route = Blueprint("charts", __name__)


@charts_route.route("/charts")
def charts():

    values = [55, 102, 100]
    plt.hist(values, bins=2)
    return render_template("charts.html", test=plt.show())

