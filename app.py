from flask import Flask, render_template, request, redirect, flash, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'something_secret_and_random'  # Needed for flash messages

# 🚗 Updated car list with uniform `category`
cars = [
    {
        'name': 'Toyota Premio',
        'slug': 'toyota-premio',
        'image': 'premio.jpg',
        'gallery': ['premio1.jpg', 'premio2.jpg', 'premio3.jpg', 'premio4.jpg', 'premio5.jpg', 'premio6.jpg'],
        'description': 'A stylish and spacious sedan with outstanding fuel efficiency, smooth ride quality, and premium interior finish.',
        'price': 'Ksh 1,200,000',
        'category': 'Sedan',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Mazda Demio',
        'slug': 'mazda-demio',
        'image': 'demio.jpg',
        'gallery': ['demio1.jpg', 'demio2.jpg', 'demio3.jpg', 'demio4.jpg', 'demio5.jpg', 'demio6.jpg'],
        'description': 'A compact hatchback known for agility, great handling, and dependable performance — ideal for urban driving.',
        'price': 'Ksh 750,000',
        'category': 'Economy',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Subaru Impreza',
        'slug': 'subaru-impreza',
        'image': 'impreza.jpg',
        'gallery': ['impreza1.jpg', 'impreza2.jpg', 'impreza3.jpg', 'impreza4.jpg', 'impreza5.jpg', 'impreza6.jpg'],
        'description': 'Sporty and dependable with Subaru’s famous all-wheel drive. Excellent on both city roads and rough terrain.',
        'price': 'Ksh 1,000,000',
        'category': 'Sports',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Nissan Note',
        'slug': 'nissan-note',
        'image': 'note.jpg',
        'gallery': ['note1.jpg', 'note2.jpg', 'note3.jpg', 'note4.jpg', 'note5.jpg', 'note6.jpg'],
        'description': 'A practical hatchback with a roomy cabin, smart technology, and superb fuel economy — perfect for families.',
        'price': 'Ksh 650,000',
        'category': 'Economy',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Honda Fit',
        'slug': 'honda-fit',
        'image': 'fit.jpg',
        'gallery': ['fit1.jpg', 'fit2.jpg', 'fit3.jpg', 'fit4.jpg', 'fit5.jpg', 'fit6.jpg'],
        'description': 'Reliable, compact, and impressively fuel-efficient. The Honda Fit delivers versatility and comfort on a budget.',
        'price': 'Ksh 700,000',
        'category': 'Economy',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Volkswagen Golf',
        'slug': 'volkswagen-golf',
        'image': 'golf.jpg',
        'gallery': ['golf1.jpg', 'golf2.jpg', 'golf3.jpg', 'golf4.jpg', 'golf5.jpg', 'golf6.jpg'],
        'description': 'A premium hatchback with excellent build quality, sporty handling, and top-tier interior features.',
        'price': 'Ksh 1,100,000',
        'category': 'Luxury',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Toyota Vitz',
        'slug': 'toyota-vitz',
        'image': 'vitz.jpg',
        'gallery': ['vitz1.jpg', 'vitz2.jpg', 'vitz3.jpg', 'vitz4.jpg', 'vitz5.jpg', 'vitz6.jpg'],
        'description': 'Economical and easy to park, this compact hatchback is perfect for new drivers or busy city life.',
        'price': 'Ksh 600,000',
        'category': 'Economy',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Suzuki Swift',
        'slug': 'suzuki-swift',
        'image': 'swift.jpg',
        'gallery': ['swift1.jpg', 'swift2.jpg', 'swift3.jpg', 'swift4.jpg', 'swift5.jpg', 'swift6.jpg'],
        'description': 'A nimble and youthful car with sharp styling, good performance, and low fuel consumption.',
        'price': 'Ksh 650,000',
        'category': 'Economy',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'BMW 3 Series',
        'slug': 'bmw-3-series',
        'image': 'bmw3.jpg',
        'gallery': ['bmw3_1.jpg', 'bmw3_2.jpg', 'bmw3_3.jpg', 'bmw3_4.jpg', 'bmw3_5.jpg', 'bmw3_6.jpg'],
        'description': 'A luxury sedan with dynamic performance, upscale interiors, and cutting-edge technology.',
        'price': 'Ksh 2,300,000',
        'category': 'Luxury',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Mercedes C-Class',
        'slug': 'mercedes-c-class',
        'image': 'cclass.jpg',
        'gallery': ['cclass1.jpg', 'cclass2.jpg', 'cclass3.jpg', 'cclass4.jpg', 'cclass5.jpg', 'cclass6.jpg'],
        'description': 'Refined, powerful, and luxurious — the C-Class is the benchmark of premium comfort and driving excellence.',
        'price': 'Ksh 2,800,000',
        'category': 'Luxury',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Toyota Harrier',
        'slug': 'toyota-harrier',
        'image': 'harrier.jpg',
        'gallery': ['harrier1.jpg', 'harrier2.jpg', 'harrier3.jpg', 'harrier4.jpg', 'harrier5.jpg', 'harrier6.jpg'],
        'description': 'A luxury SUV with a bold design, smooth power delivery, and comfortable driving for long journeys.',
        'price': 'Ksh 2,200,000',
        'category': 'SUV',
        'fuel': 'Petrol',
        'transmission': 'Automatic'
    },
    {
        'name': 'Range Rover Evoque',
        'slug': 'range-rover-evoque',
        'image': 'evoque.jpg',
        'gallery': ['evoque1.jpg', 'evoque2.jpg', 'evoque3.jpg', 'evoque4.jpg', 'evoque5.jpg', 'evoque6.jpg'],
        'description': 'A premium compact SUV with a striking design, luxury features, and strong off-road capabilities.',
        'price': 'Ksh 3,500,000',
        'category': 'SUV',
        'fuel': 'Diesel',
        'transmission': 'Automatic'
    }
]


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

    filename = os.path.join('static', 'bookings.csv')
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Email", "Phone", "Payment", "Date", "Car"])
        writer.writerow([name, email, phone, payment, date, car])

    flash("Booking submitted successfully!", "success")
    return redirect(url_for("thank_you", name=name, car=car))


@app.route("/thankyou")
def thank_you():
    name = request.args.get("name")
    car = request.args.get("car")
    return render_template("thankyou.html", name=name, car=car)


@app.route("/bookings")
def view_bookings():
    filename = os.path.join('static', 'bookings.csv')
    bookings = []
    headers = ["Name", "Email", "Phone", "Payment", "Date", "Car"]

    if os.path.isfile(filename):
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            bookings = list(reader)

    return render_template("bookings.html", bookings=bookings, headers=headers)


@app.route("/delete/<int:index>")
def delete_booking(index):
    filename = os.path.join('static', 'bookings.csv')
    if os.path.isfile(filename):
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = list(csv.reader(file))
            headers = reader[0]
            bookings = reader[1:]

        if 0 <= index < len(bookings):
            del bookings[index]
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(bookings)
            flash("Booking deleted successfully.", "success")
        else:
            flash("Invalid booking index.", "danger")

    return redirect(url_for("view_bookings"))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
