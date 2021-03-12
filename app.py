from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, datetime
from statistic import plot
UPLOAD_FOLDER = os.path.abspath('static')

app = Flask(__name__)
app.register_blueprint(plot)
app.secret_key = "gaighaoehghwah"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

def saveDate():
    try:
        f= open('date.txt', 'a')
    except:
        print('Could not open a file')
        quit()
    dateNow = datetime.datetime.now()
    f.write(dateNow.strftime("%m.%d,"))
def calculateSum(exp):
    sum = 0
    for i in exp:
        if i.char == "+":
            sum+=i.price
        else:
            sum-=i.price
    return sum
def saveToFile(exp):
    try:
        f= open('data.txt', 'a')
    except:
        print('nie udało się otworzyć pliku')
        quit()
    f.write(str(calculateSum(exp))+',')
    f.close()

class Expenses(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    char = db.Column(db.String(10))
    price = db.Column(db.Float)
    path_to_img = db.Column(db.String(300))

    def __init__(self,name,char,price,path_to_img):
        self.name = name
        self.char = char
        self.price = price
        self.path_to_img = path_to_img

@app.route('/wydatki', methods=['POST','GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        char = request.form['value']
        price = request.form['price']
        img = request.files['img']
        if img.filename == "":
            flash("Nie wybrano zdjęcia")
        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'],'images', filename))
        expenses = Expenses(name, char, price, img.filename)
        db.session.add(expenses)
        db.session.commit()
        exp = Expenses.query.all()
        saveToFile(exp)
        saveDate()
        return redirect(url_for('home'))
    else:
        all_spendings = 0
        exp = Expenses.query.all()
        sum = calculateSum(exp)
        return render_template('wydatki.html',all_spendings=round(sum,2),expen = Expenses, expenses=exp, path=os.path.join('images',""))

@app.route('/deleteRecord', methods=["POST", "GET"])
def deleteRecord():
    if request.method == 'POST':
        id_to_delete = request.form['id']
        delete = Expenses.query.filter_by(_id=id_to_delete).first()
        print(id_to_delete)
        db.session.delete(delete)
        db.session.commit()
    return redirect(url_for("home"))
@app.route('/<page>')
def dif(page):
    return '<center><h1>strona '+page+' nie jest jeszcze skończona</h1></center>'
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

