from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'something_secret_and_random'  # Needed for flash messages

# 🚀 Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 📦 Database Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    payment = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    car = db.Column(db.String(100), nullable=False)

# 🚗 Car list (add your cars here)
cars = [
    {
        "name": "BMW 3 Series",
        "slug": "bmw-3-series",
        "image": "bmw3.jpg",
        "description": "A sporty and luxurious sedan with excellent handling.",
        "price": "KSh 6,500/day",
        "category": "Sedan",
        "fuel": "Petrol",
        "transmission": "Automatic"
    },
    {
        "name": "Mercedes C-Class",
        "slug": "mercedes-c-class",
        "image": "cclass.jpg",
        "description": "Executive sedan with comfort and elegance for city or highway.",
        "price": "KSh 7,000/day",
        "category": "Sedan",
        "fuel": "Petrol",
        "transmission": "Automatic"
    },
    {
        "name": "Mazda Demio",
        "slug": "mazda-demio",
        "image": "demio.jpg",
        "description": "A popular compact hatchback perfect for city drives.",
        "price": "KSh 3,200/day",
        "category": "Hatchback",
        "fuel": "Petrol",
        "transmission": "Automatic"
    },
    {
        "name": "Range Rover Evoque",
        "slug": "range-rover-evoque",
        "image": "evoque.jpg",
        "description": "Stylish luxury SUV with top-tier comfort and power.",
        "price": "KSh 9,500/day",
        "category": "SUV",
        "fuel": "Diesel",
        "transmission": "Automatic"
    },
    {
        "name": "Honda Fit",
        "slug": "honda-fit",
        "image": "fit.jpg",
        "description": "A versatile subcompact car known for space and efficiency.",
        "price": "KSh 3,800/day",
        "category": "Hatchback",
        "fuel": "Hybrid",
        "transmission": "Automatic"
    },
    {
        "name": "Volkswagen Golf",
        "slug": "vw-golf",
        "image": "golf.jpg",
        "description": "A stylish hatch with great performance and tech.",
        "price": "KSh 4,200/day",
        "category": "Hatchback",
        "fuel": "Petrol",
        "transmission": "Manual"
    },
    {
        "name": "Toyota Harrier",
        "slug": "toyota-harrier",
        "image": "harrier.jpg",
        "description": "Spacious and premium SUV, ideal for family travel.",
        "price": "KSh 6,800/day",
        "category": "SUV",
        "fuel": "Petrol",
        "transmission": "Automatic"
    },
    {
        "name": "Subaru Impreza",
        "slug": "subaru-impreza",
        "image": "impreza.jpg",
        "description": "Reliable AWD sedan with sporty edge and safety.",
        "price": "KSh 5,000/day",
        "category": "Sedan",
        "fuel": "Petrol",
        "transmission": "Manual"
    },
    {
        "name": "Nissan Note",
        "slug": "nissan-note",
        "image": "note.jpg",
        "description": "Fuel-efficient hatchback with smart interior layout.",
        "price": "KSh 3,600/day",
        "category": "Hatchback",
        "fuel": "Petrol",
        "transmission": "Automatic"
    },
    {
        "name": "Toyota Premio",
        "slug": "toyota-premio",
        "image": "premio.jpg",
        "description": "A mid-size sedan blending reliability and comfort.",
        "price": "KSh 4,800/day",
        "category": "Sedan",
        "fuel": "Petrol",
        "transmission": "Automatic"
    }
]

# Debug helper to list all expected image names
for car in cars:
    print(car["image"])



@app.route("/")
def home():
    query = request.args.get('search', '').lower()
    selected_category = request.args.get('category')
    selected_fuel = request.args.get('fuel')

    car_categories = sorted(set(car['category'] for car in cars))
    fuel_types = sorted(set(car['fuel'] for car in cars))

    filtered_cars = [
        car for car in cars
        if (not query or query in car['name'].lower())
        and (not selected_category or car['category'] == selected_category)
        and (not selected_fuel or car['fuel'] == selected_fuel)
    ]

    return render_template(
        "index.html",
        cars=filtered_cars,
        car_categories=car_categories,
        fuel_types=fuel_types,
        selected_category=selected_category,
        selected_fuel=selected_fuel,
        query=query
    )

@app.route("/car/<slug>")
def car_detail(slug):
    car = next((c for c in cars if c.get('slug') == slug), None)
    if not car:
        return "Car not found", 404
    return render_template('car_detail.html', car=car)

@app.route("/book/<car_name>")
def book(car_name):
    car_data = next((car for car in cars if car['name'] == car_name), None)
    car_image = car_data['image'] if car_data else "placeholder.jpg"
    return render_template("book.html", car=car_data, car_image=car_image)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    payment = request.form.get("payment")
    date = request.form.get("date")
    car = request.form.get("car")

    if not all([name, email, phone, payment, date, car]):
        flash("Please fill in all fields.", "danger")
        return redirect(url_for("book", car_name=car))

    existing = Booking.query.filter_by(car=car, date=date).first()
    if existing:
        flash("Sorry, this car is already booked on that date.", "danger")
        return redirect(url_for("book", car_name=car))

    new_booking = Booking(
        name=name,
        email=email,
        phone=phone,
        payment=payment,
        date=date,
        car=car
    )
    db.session.add(new_booking)
    db.session.commit()

    flash("Booking submitted successfully!", "success")
    return redirect(url_for("thank_you", name=name, car=car))

@app.route("/thankyou")
def thank_you():
    name = request.args.get("name")
    car = request.args.get("car")
    return render_template("thankyou.html", name=name, car=car)

@app.route("/bookings")
def view_bookings():
    bookings = Booking.query.all()
    return render_template("bookings.html", bookings=bookings)

@app.route("/delete/<int:booking_id>")
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted successfully.", "success")
    return redirect(url_for("view_bookings"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)
