from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.secret_key = "secret"
app.config['BILL_SAVE_PATH'] = r"D:\Vs"  # Bill save directory

db = SQLAlchemy(app)

# 🧑 User Model (for login)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# 🥛 Milk Details Model
class Milk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    milk_type = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

# 🏪 Vendor Details Model
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(10), nullable=False, unique=True)

# 🧾 Bill Model (Updated)
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(10), unique=True, nullable=False)
    vendor_id = db.Column(db.Integer, nullable=False)
    milk_type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

# 🌟 Initialize database
with app.app_context():
    db.create_all()

    # Insert a default user if none exists
    if User.query.count() == 0:
        hashed_pw = generate_password_hash("admin123", method="pbkdf2:sha256")
        default_user = User(username="admin", password=hashed_pw)
        db.session.add(default_user)

    # Insert Default Milk Data (if not exists)
    if Milk.query.count() == 0:
        default_milk = [
            Milk(milk_type="Cow", price=40.0),
            Milk(milk_type="Buffalo", price=50.0),
            Milk(milk_type="Goat", price=60.0)
        ]
        db.session.bulk_save_objects(default_milk)

    db.session.commit()

# 🏠 Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

# 🏠 Dashboard (Requires Login)
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# 🥛 Milk Details Page (Edit & Save Price)
@app.route('/milk_details', methods=['GET', 'POST'])
def milk_details():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        milk_id = request.form['milk_id']
        new_price = request.form['new_price']

        milk = Milk.query.get(milk_id)
        if milk:
            milk.price = float(new_price)
            db.session.commit()
            flash("Price updated successfully!", "success")

    milk_records = Milk.query.all()
    return render_template('milk_details.html', milk_records=milk_records)

# 🏪 Vendor Details Page (Auto ID & Validation)
@app.route('/vendor_details', methods=['GET', 'POST'])
def vendor_details():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']

        if len(contact) != 10 or not contact.isdigit() or contact[0] < '5':
            flash("Invalid Contact Number! Must be 10 digits and start with 5 or higher.", "danger")
        else:
            new_vendor = Vendor(name=name, contact=contact)
            db.session.add(new_vendor)
            db.session.commit()
            flash("Vendor added successfully!", "success")

    vendors = Vendor.query.all()
    return render_template('vendor_details.html', vendors=vendors)

# 📜 Bill Page (Generate Bill)
@app.route('/bill', methods=['GET', 'POST'])
def bill():
    if 'user' not in session:
        return redirect(url_for('login'))

    milk_types = Milk.query.all()
    milk_prices = {milk.milk_type: milk.price for milk in milk_types}
    generated_bill = None

    if request.method == 'POST':
        bill_no = f"BILL{random.randint(1000, 9999)}"
        vendor_id = request.form['vendor_id']
        milk_type = request.form['milk_type']
        quantity = float(request.form['quantity'])

        vendor = Vendor.query.get(vendor_id)
        if not vendor:
            flash("Vendor ID not found! Please register the vendor first.", "danger")
            return redirect(url_for('vendor_details'))

        milk = Milk.query.filter_by(milk_type=milk_type).first()
        if milk:
            total_price = quantity * milk.price
            new_bill = Bill(
                bill_no=bill_no,
                vendor_id=vendor_id,
                milk_type=milk_type,
                quantity=quantity,
                total_price=total_price,
                timestamp=datetime.now()
            )
            db.session.add(new_bill)
            db.session.commit()
            generated_bill = new_bill
            flash(f"Bill {bill_no} generated successfully!", "success")

    return render_template('bill.html', 
                         milk_types=milk_types, 
                         milk_prices=milk_prices, 
                         generated_bill=generated_bill)

# 📜 Bill Details Page
@app.route('/bill_details', methods=['GET', 'POST'])
def bill_details():
    if 'user' not in session:
        return redirect(url_for('login'))

    bill = None

    if request.method == 'POST':
        bill_no = request.form['bill_no']
        bill = Bill.query.filter_by(bill_no=bill_no).first()

        if not bill:
            flash("Bill not found! Please enter a valid Bill Number.", "danger")

    return render_template('bill_details.html', bill=bill)

# 🖨️ Generate Bill PDF
@app.route('/generate_bill_image', methods=['POST'])
def generate_bill_image():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    bill_no = request.form['bill_no']
    bill = Bill.query.filter_by(bill_no=bill_no).first()
    vendor = Vendor.query.get(bill.vendor_id) if bill else None
    
    if not bill or not vendor:
        flash("Bill or vendor not found!", "danger")
        return redirect(url_for('bill'))
    
    # Create directory if it doesn't exist
    if not os.path.exists(app.config['BILL_SAVE_PATH']):
        os.makedirs(app.config['BILL_SAVE_PATH'])
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"Bill_{bill_no}_{timestamp}.pdf"
    filepath = os.path.join(app.config['BILL_SAVE_PATH'], filename)
    
    # Create PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Bill Header
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "DAIRY MANAGEMENT SYSTEM")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-80, f"BILL #{bill_no}")
    
    # Bill Details
    c.setFont("Helvetica", 12)
    y_position = height - 120
    details = [
        f"Date: {bill.timestamp.strftime('%d-%m-%Y %H:%M')}",
        f"Vendor: {vendor.name} (ID: {vendor.id})",
        f"Contact: {vendor.contact}",
        f"Milk Type: {bill.milk_type}",
        f"Quantity: {bill.quantity} Liters",
        f"Price per Liter: ₹{Milk.query.filter_by(milk_type=bill.milk_type).first().price}",
        f"Total Amount: ₹{bill.total_price}"
    ]
    
    for line in details:
        c.drawString(100, y_position, line)
        y_position -= 25
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 50, "Thank you for your business!")
    
    c.save()
    
    flash(f"Bill PDF saved successfully at {filepath}", "success")
    return redirect(url_for('bill_details', bill_no=bill_no))

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)