import matplotlib.pyplot as plt
import numpy
from flask import Blueprint, Flask, url_for, redirect, render_template
import os, time, json, glob
plot = Blueprint('plot', __name__, static_folder="static", template_folder="templates")

@plot.route("/podsumowanie")
def podsumowanie():
	data = list()
	for f in  glob.glob("*.json"):
		x = json.load(f)
		data.append([x])
	return f'<h1>{data}</h1>'
#    plt.plot(date,data, color="pink", linewidth=3)
 #   plt.savefig(os.path.join('static', 'plot.png'))
  #  t = time.time()
   # return render_template("plot.html", t=t)

