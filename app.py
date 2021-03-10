from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.abspath('static')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)



class Expenses(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    path_to_img = db.Column(db.String(300))

    def __init__(self,name,price,path_to_img):
        self.name = name
        self.price = price
        self.path_to_img = path_to_img


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        img = request.files['img']
        if img.filename == "":
            flash("Nie wybrano zdjęcia")
        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'],'images', filename))
        expenses = Expenses(name,price, img.filename)
        db.session.add(expenses)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        exp = Expenses.query.all()
        return render_template('wydatki.html', expenses=exp, path=os.path.join('images',""))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

