import matplotlib.pyplot as plt
import numpy
from flask import Blueprint, Flask, url_for, redirect, render_template
import os, time
plot = Blueprint('plot', __name__, static_folder="static", template_folder="templates")

@plot.route("/podsumowanie")
def podsumowanie():
    data = numpy.genfromtxt("data.txt", delimiter=',')
    date = numpy.genfromtxt("date.txt", delimiter=',', dtype="|S5")
    print(data)
    print(date)
    plt.plot(date,data, color="pink", linewidth=3)
    plt.savefig(os.path.join('static', 'plot.png'))
    t = time.time()
    return render_template("plot.html", t=t)

