import matplotlib.pyplot as plt
import numpy
from flask import Blueprint, Flask, url_for, redirect

plot = Blueprint('plot', __name__, static_folder="static", template_folder="templates")

@plot.route("/podsumowanie")
def podsumowanie():
    data = numpy.genfromtxt("data.txt", delimiter=',')
    date = numpy.genfromtxt("date.txt", delimiter=',', dtype="|S5")
    print(data)
    print(date)
    plt.plot(date,data)
    plt.show()
    return redirect(url_for("home"))

