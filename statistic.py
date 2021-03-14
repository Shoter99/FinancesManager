import matplotlib.pyplot as plt
import numpy, os
from flask import Blueprint, Flask, url_for, redirect, render_template

plot = Blueprint('plot', __name__)

@plot.route("/podsumowanie")
def podsumowanie():
    try:
        data = numpy.genfromtxt("data.txt", delimiter=',')
        date = numpy.genfromtxt("date.txt", delimiter=',', dtype="|S5")
    except Exception as e:
        print(e)
        data = 0
        date = ''
    plt.plot(date,data, color='pink', linewidth=3.0)
    plt.savefig(os.path.join('static', 'plot.png'))
    return render_template('plot.html')

