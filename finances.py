from flask import Blueprint, request, redirect, render_template, flash, url_for
from db_models import Category, Expenses
from db_shared import db
from functions import saveDate, calculateSum, saveToFile, UPLOAD_FOLDER
import os
finances = Blueprint('finances', __name__)

@finances.route('/wydatki', methods=['POST','GET'])
@finances.route('/', methods=['POST', 'GET'])
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
            img.save(os.path.join(UPLOAD_FOLDER,'images', filename))
        find_category = Category.query.filter_by(category_name = category).first()
        expenses = Expenses(name, char, price, img.filename, find_category._id)    
        db.session.add(expenses)
        db.session.commit()
        exp = Expenses.query.all()
        saveToFile(exp)
        saveDate()
        return redirect(url_for('finances.home'))
    else:
        all_spendings = 0
        exp = Expenses.query.all()
        cat = Category.query.all()
        category_sum = dict()
        for c in cat:
            category_sum.update({c.category_name: calculateSum(c.expenses)})
        print(category_sum)
        return render_template('wydatki.html',all_spendings=category_sum,category=cat,expen = Expenses, expenses=exp, path=os.path.join('images',""))
@finances.route('/createCategory', methods=['POST', 'GET'])
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
        return redirect(url_for('finances.home'))
    else:
        return redirect(url_for('finances.home'))


@finances.route('/deleteRecord', methods=["POST", "GET"])
def deleteRecord():
    if request.method == 'POST':
        #deleting Record from database with id specified in form
        id_to_delete = request.form['id']
        delete = Expenses.query.filter_by(_id=id_to_delete).first()
        db.session.delete(delete)
        db.session.commit()
    return redirect(url_for("finances.home"))