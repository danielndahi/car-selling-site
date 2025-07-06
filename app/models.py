from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    payment = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    car = db.Column(db.String(100), nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    fuel = db.Column(db.String(50), nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    lease_price = db.Column(db.String(50), nullable=False)
    purchase_price = db.Column(db.String(50), nullable=False)
