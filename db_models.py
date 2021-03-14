from db_shared import db

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