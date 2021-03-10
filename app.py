from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        return '<h1>Hello this is from post</h1>'
    else:
        return render_template('wydatki.html')

if __name__ == '__main__':
    app.run(debug=True)

