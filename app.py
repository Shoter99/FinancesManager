from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, datetime, json
from statistic import plot
from db_shared import db
from finances import finances
#defining a folder for images
from functions import UPLOAD_FOLDER

app = Flask(__name__)
app.register_blueprint(plot)
app.register_blueprint(finances)
app.secret_key = "gaighaoehghwah"
#setting up a database finances.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

#creating a route which will users be directed to if the page that he tries to enter is not yet avaiable
@app.route('/<page>')
def dif(page):
    return '<center><h1>strona '+page+' nie jest jeszcze skończona</h1></center>'

#creating database and running an app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

