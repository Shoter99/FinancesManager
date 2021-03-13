from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, datetime
from statistic import plot
#defining a folder for images
UPLOAD_FOLDER = os.path.abspath('static')

app = Flask(__name__)
app.register_blueprint(plot)
app.secret_key = "gaighaoehghwah"
#setting up a database finances.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
#creating a function that saves current date to a file
def saveDate():
    try:
        f= open('date.txt', 'a')
    except:
        print('Could not open a file')
        quit()
    dateNow = datetime.datetime.now()
    f.write(dateNow.strftime("%m.%d,"))
#creating a function that calcuates all spendings and expenses
def calculateSum(exp):
    sum = 0
    for i in exp:
        if i.char == "+":
            sum+=i.price
        else:
            sum-=i.price
    return sum
#saving the calculations from previous function to a file
def saveToFile(exp):
    try:
        f= open('data.txt', 'a')
    except:
        print('nie udało się otworzyć pliku')
        quit()
    f.write(str(calculateSum(exp))+',')
    f.close()
#creating category class 
#that stores name of the category and is in one to many relationship 
class Category(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    category_name = db.Column(db.String(200))
    expenses = db.relationship('Expenses', backref='category', lazy=True)

    def __init__(self, category_name):
        self.category_name = category_name
#this class stores name, char, price and path to image
#it is also connected to Category table
class Expenses(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    #char defines if user gain some money or spend it
    #this column will hold + or - 
    char = db.Column(db.String(10))
    price = db.Column(db.Float)
    path_to_img = db.Column(db.String(300))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self,name,char,price,path_to_img, category_id):
        self.name = name
        self.char = char
        self.price = price
        self.path_to_img = path_to_img
        self.category_id = category_id

@app.route('/wydatki', methods=['POST','GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        #taking input from form and saving it to database
        category = request.form['category']
        name = request.form['name']
        char = request.form['value']
        price = request.form['price']
        img = request.files['img']
        if img.filename == "":
            flash("Nie wybrano zdjęcia")
        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'],'images', filename))
        find_category = Category.query.filter_by(category_name = category).first()
        expenses = Expenses(name, char, price, img.filename, find_category._id)    
        db.session.add(expenses)
        db.session.commit()
        exp = Expenses.query.all()
        saveToFile(exp)
        saveDate()
        return redirect(url_for('home'))
    else:
        all_spendings = 0
        exp = Expenses.query.all()
        cat = Category.query.all()
        category_sum = dict()
        for c in cat:
            category_sum.update({c.category_name: calculateSum(c.expenses)})
        print(category_sum)
        return render_template('wydatki.html',all_spendings=category_sum,category=cat,expen = Expenses, expenses=exp, path=os.path.join('images',""))


@app.route('/createCategory', methods=['POST', 'GET'])
def createCategory():
    if request.method == 'POST':
        category = request.form['category']
        find_category = Category.query.filter_by(category_name=category).first()
        if find_category:
            flash('This category already exists')
            return redirect(url_for('home'))
        new_Category = Category(category)
        db.session.add(new_Category)
        db.session.commit()
        flash('New category has been created')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/deleteRecord', methods=["POST", "GET"])
def deleteRecord():
    if request.method == 'POST':
        #deleting Record from database with id specified in form
        id_to_delete = request.form['id']
        delete = Expenses.query.filter_by(_id=id_to_delete).first()
        db.session.delete(delete)
        db.session.commit()
    return redirect(url_for("home"))
#creating a route which will users be directed to if the page that he tries to enter is not yet avaiable
@app.route('/<page>')
def dif(page):
    return '<center><h1>strona '+page+' nie jest jeszcze skończona</h1></center>'

#creating database and running an app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

