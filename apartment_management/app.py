# from datetime import datetime
# import re
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# import mysql.connector
# from werkzeug.security import generate_password_hash, check_password_hash
# import random
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from config import db_config
# import os

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # Configure MySQL
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Het@1305",
#     database="flask_app"
# )
# cursor = db.cursor()


# # Database configuration (replace with your own credentials)
# db_config = {
#     'user': os.getenv('root', 'root'),
#     'password': os.getenv('Het@1305', 'Het@1305'),
#     'host': os.getenv('localhost', 'localhost'),
#     'database': os.getenv('flask_app', 'flask_app')
# }

# # Helper functions for OTP generation and sending email
# def generate_otp():
#     return str(random.randint(100000, 999999))

# def send_otp(email, otp):
#     try:
#         sender_email = "hetkothari2005@gmail.com"  # Your Gmail address
#         sender_password = "hgbh nuvn zfcw mtsu"    # App password generated
#         subject = "Your OTP for Password Reset"
        
#         message = MIMEMultipart()
#         message["From"] = sender_email
#         message["To"] = email
#         message["Subject"] = subject
#         body = f"Your OTP for password reset is: {otp}"
#         message.attach(MIMEText(body, "plain"))

#         # Use Gmail's SMTP server
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, email, message.as_string())
#         return True
#     except Exception as e:
#         print("Error sending OTP email:", e)
#         return False

# @app.route('/', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         try:
#             username = request.form['username']
#             password = generate_password_hash(request.form['password'])
#             email = request.form['email']
#             first_name = request.form['first_name']
#             last_name = request.form['last_name']
#             age = request.form['age']

#             # Check if username already exists
#             cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
#             existing_user = cursor.fetchone()

#             if existing_user:
#                 flash("Username already exists. Please choose a different username.", "danger")
#                 return redirect(url_for('register'))

#             # Insert user data into the database
#             cursor.execute("INSERT INTO user (username, password, email, first_name, last_name, age) VALUES (%s, %s, %s, %s, %s, %s)",
#                            (username, password, email, first_name, last_name, age))
#             db.commit()

#             flash("Registration successful! Please log in.", "success")
#             return redirect(url_for('login'))
#         except Exception as e:
#             print("Error during registration:", e)
#             flash("An error occurred. Please try again later.", "danger")
#             return redirect(url_for('register'))
#     return render_template('register.html')

# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
        

# #         login_cursor = db.cursor()
# #         login_cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
# #         user = cursor.fetchone()
# #         login_cursor.fetchall() 

# #         if user and check_password_hash(user[2], password):
# #             session['user_id'] = user[0]
# #             flash("Login successful!", "success")
# #             return redirect(url_for('dashboard'))
# #         else:
# #             flash("Invalid username or password.", "danger")
    
# #     return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         try:
#             # Use a new cursor for each query
#             login_cursor = db.cursor()
#             login_cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
#             user = login_cursor.fetchone()
#             login_cursor.close()  # Close cursor after use

#             # Check if user exists and validate password
#             if user and check_password_hash(user[2], password):
#                 session['user_id'] = user[0]
#                 flash("Login successful!", "success")
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash("Invalid username or password.", "danger")

#         except mysql.connector.Error as err:
#             print(f"Error: {err}")  # Print the error for debugging
#             flash("An error occurred while trying to log in.", "danger")
    
#     return render_template('login.html')


# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('dashboard.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash("Logged out successfully.", "success")
#     return redirect(url_for('login'))

# # Forgot password routes
# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email']
#         cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
#         user = cursor.fetchone()

#         if user:
#             otp = generate_otp()
#             session['otp'] = otp
#             session['email'] = email

#             if send_otp(email, otp):
#                 flash("OTP has been sent to your email.", "success")
#                 return redirect(url_for('verify_otp'))
#             else:
#                 flash("Failed to send OTP. Please try again.", "danger")
#         else:
#             flash("Email not found.", "danger")
#     return render_template('forgot_password.html')

# @app.route('/verify_otp', methods=['GET', 'POST'])
# def verify_otp():
#     if request.method == 'POST':
#         otp_entered = request.form['otp']
#         if otp_entered == session.get('otp'):
#             flash("OTP verified. You can reset your password.", "success")
#             return redirect(url_for('reset_password'))
#         else:
#             flash("Invalid OTP. Please try again.", "danger")
#     return render_template('verify_otp.html')

# # @app.route('/reset_password', methods=['GET', 'POST'])
# # def reset_password():
# #     if 'email' not in session:
# #         return redirect(url_for('login'))

# #     if request.method == 'POST':
# #         new_password = generate_password_hash(request.form['password'])
# #         email = session['email']
        
# #         cursor.execute("UPDATE user SET password=%s WHERE email=%s", (new_password, email))
# #         db.commit()

# #         # Clear session after password reset
# #         session.pop('email', None)
# #         session.pop('otp', None)

# #         flash("Your password has been reset successfully. Please log in.", "success")
# #         return redirect(url_for('login'))
# #     return render_template('reset_password.html')

# @app.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     if 'email' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         new_password = generate_password_hash(request.form['password'])
#         email = session['email']
        
#         # cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
#         # cursor.fetchall()  # Clear any results to avoid 'Unread result found'
        
#         # cursor.execute("UPDATE user SET password=%s WHERE email=%s", (new_password, email))
#         # db.commit()

#         # Clear session after password reset
#         session.pop('email', None)
#         session.pop('otp', None)

#         flash("Your password has been reset successfully. Please log in.", "success")
#         return redirect(url_for('login'))
#     return render_template('reset_password.html')

# # Tenant Management Routes
# # @app.route('/tenants', methods=['GET', 'POST'])
# # def manage_tenants():
# #     if 'user_id' not in session:
# #         return redirect(url_for('login'))

# #     if request.method == 'POST':
# #         tenant_name = request.form['tenant_name']
# #         apartment_number = request.form['apartment_number']
# #         # cursor.execute("INSERT INTO tenants (name, apartment_number) VALUES (%s, %s)", (tenant_name, apartment_number))
# #         cursor.execute("INSERT INTO tenants (name) VALUES (%s)", (tenant_name,))
# #         db.commit()
# #         flash("Tenant added successfully!", "success")

# #     cursor.execute("SELECT * FROM tenants")
# #     tenants = cursor.fetchall()


# # Function to validate phone number format
# # def is_valid_phone(phone):
# #     return re.match(r"^\+?\d{10,15}$", phone) is not None

# # def manage_tenants():
# #     cursor = db.cursor()

# #     if request.method == "POST":
# #         tenant_name = request.form["tenant_name"]
# #         apartment_id = request.form["apartment_number"]
# #         lease_start_date = request.form["lease_start_date"]
# #         lease_end_date = request.form["lease_end_date"]
# #         contact_info = request.form["contact_info"]

# #         # Validate phone number
# #         if not is_valid_phone(contact_info):
# #             return "Invalid phone number format. Please enter a valid number."

# #         # Insert new tenant into the database
# #         cursor.execute(
# #             "INSERT INTO tenants (name, apartment_id, lease_start_date, lease_end_date, contact_info) VALUES (%s, %s, %s, %s, %s)",
# #             (tenant_name, apartment_id, lease_start_date, lease_end_date, contact_info)
# #         )
# #         db.commit()

# #         return redirect(url_for("manage_tenants"))
    
# #     # Retrieve current tenants
# #     cursor.execute("SELECT * FROM tenants")
# #     tenants = cursor.fetchall()
# #     cursor.close()

# #     # return redirect(url_for("manage_tenants"))

# #     # # Retrieve current tenants
# #     # cursor.execute("SELECT * FROM tenants")
# #     # tenants = cursor.fetchall()
# #     # cursor.close()

# #     return render_template('tenants.html', tenants=tenants)

# # Function to validate phone number format
# def is_valid_phone(phone):
#     return re.match(r"^\+?\d{10,15}$", phone) is not None

# @app.route("/tenants", methods=["GET", "POST"])
# def manage_tenants():
#     cursor = db.cursor()

#     if request.method == "POST":
#         tenant_name = request.form["tenant_name"]
#         apartment_id = request.form["apartment_number"]
#         lease_start_date = request.form["lease_start_date"]
#         lease_end_date = request.form["lease_end_date"]
#         contact_info = request.form["contact_info"]

#         # Validate phone number
#         if not is_valid_phone(contact_info):
#             return "Invalid phone number format. Please enter a valid number."

#         # Insert new tenant into the database
#         cursor.execute(
#             "INSERT INTO tenants (name, apartment_id, lease_start_date, lease_end_date, contact_info) VALUES (%s, %s, %s, %s, %s)",
#             (tenant_name, apartment_id, lease_start_date, lease_end_date, contact_info)
#         )
#         db.commit()

#         return redirect(url_for("manage_tenants"))

#     # Retrieve current tenants
#     cursor.execute("SELECT * FROM tenants")
#     tenants = cursor.fetchall()
#     cursor.close()

#     return render_template("tenants.html", tenants=tenants)
# # Apartment Listings Routes
# @app.route('/apartments')
# def apartments():
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM apartments")
#     apartments = cursor.fetchall()
#     conn.close()
#     return render_template('apartments.html', apartments=apartments)
# @app.route('/add_apartment', methods=['GET', 'POST'])
# def add_apartment():
#     if request.method == 'POST':
#         apartment_name = request.form.get('apartment_name').strip()
#         apartment_location = request.form.get('apartment_location').strip()
#         apartment_price = request.form.get('apartment_price').strip()

#         # Validate input
#         if not apartment_name or not apartment_location or not apartment_price:
#             flash('All fields are required!', 'danger')
#             return redirect(url_for('add_apartment'))

#         try:
#             # Assuming `db_connection` is your database connection object
#             cursor = db.cursor()
#             query = "INSERT INTO apartments (name, location, price) VALUES (%s, %s, %s)"
#             cursor.execute(query, (apartment_name, apartment_location, apartment_price))
#             db.commit()
#             flash('Apartment added successfully!', 'success')
#         except Exception as e:
#             print(f"Error: {e}")  # Print error for debugging
#             flash('Error adding apartment. Please try again.', 'danger')
#         finally:
#             cursor.close()

#         return redirect(url_for('apartments'))  # Redirect to apartments page
        


 

#     # if request.method == 'POST':
#     #     # Retrieve form data
#     #     apartment_name = request.form['apartment_name']
#     #     apartment_location = request.form['apartment_location']
#     #     apartment_price = request.form['apartment_price']

#     #     # Add the apartment to the database
#     #     try:
#     #         conn = mysql.connector.connect(**db_config)
#     #         cursor = conn.cursor()
#     #         cursor.execute("INSERT INTO apartment$ (name, location, price) VALUES (%s, %s, %s)",
#     #                        (apartment_name, apartment_location, apartment_price))
#     #         conn.commit()
#     #         flash('Apartment added successfully!', 'success')
#     #     except mysql.connector.Error as err:
#     #         flash(f'Error: {err}', 'danger')
#     #     finally:
#     #         cursor.close()
#     #         conn.close()

#     #     return redirect(url_for('add_apartment'))

#     # return render_template('add_apartment.html')

# # @app.route('/apartments')
# # def apartments():
# #     if 'user_id' not in session:
# #         return redirect(url_for('login'))

# #     cursor.execute("SELECT * FROM apartments")
# #     apartments = cursor.fetchall()
# #     return render_template('apartments.html', apartments=apartments)


# # Route to display apartments
# # @app.route('/apartments', methods=['GET', 'POST'])
# # def apartments():
# #     conn = mysql.connector.connect(**db_config)
# #     cursor = conn.cursor()

# #     if request.method == 'POST':
# #         # Add a new apartment
# #         number = request.form['number']
# #         status = request.form['status']
# #         rent = request.form['rent']
        
# #         cursor.execute(
# #             "INSERT INTO apartments (number, status, rent) VALUES (%s, %s, %s)",
# #             (number, status, rent)
# #         )
# #         conn.commit()

# #     # Retrieve apartments
# #     cursor.execute("SELECT * FROM apartments")
# #     apartments = cursor.fetchall()

# #     cursor.close()
# #     conn.close()
    
# #     return render_template('apartments.html', apartments=apartments)

# # # Route to add an apartment directly
# # @app.route('/add_apartment', methods=['POST'])
# # def add_apartment():
# #     number = request.form['number']
# #     status = request.form['status']
# #     rent = request.form['rent']

# #     conn = mysql.connector.connect(**db_config)
# #     cursor = conn.cursor()
    
# #     cursor.execute(
# #         "INSERT INTO apartments (number, status, rent) VALUES (%s, %s, %s)",
# #         (number, status, rent)
# #     )
# #     conn.commit()

# #     cursor.close()
# #     conn.close()
    
# #     return redirect(url_for('apartments'))

# # Maintenance Requests Routes
# @app.route("/maintenance_requests", methods=["GET", "POST"])
# def maintenance_requests():
#     cursor = db.cursor()

#     if request.method == "POST":
#         tenant_id = request.form["tenant_id"]
#         apartment_id = request.form["apartment_id"]
#         request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         description = request.form["description"]
#         status = request.form["status"]

#         # Insert new maintenance request into the database
#         cursor.execute(
#             "INSERT INTO maintenance_requests (tenant_id, apartment_id, request_date, description, status) VALUES (%s, %s, %s, %s, %s)",
#             (tenant_id, apartment_id, request_date, description, status)
#         )
#         db.commit()

#         return redirect(url_for("maintenance_requests"))

#     # Retrieve maintenance requests from the database
#     cursor.execute("SELECT request_id, description, status FROM maintenance_requests")
#     requests = cursor.fetchall()
#     cursor.close()

#     return render_template("maintenance_requests.html", requests=requests)

# # @app.route('/maintenance_requests', methods=['GET', 'POST'])
# # def maintenance_requests():
# #     if 'user_id' not in session:
# #         return redirect(url_for('login'))

# #     if request.method == 'POST':
# #         request_description = request.form['description']
# #         cursor.execute("INSERT INTO maintenance_requests (description, status) VALUES (%s, 'pending')", (request_description,))
# #         db.commit()
# #         flash("Maintenance request submitted!", "success")

# #     cursor.execute("SELECT * FROM maintenance_requests")
# #     requests = cursor.fetchall()
# #     return render_template('maintenance_requests.html', requests=requests)

# # Profile Management Route
# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     cursor.execute("SELECT * FROM user WHERE id=%s", (session['user_id'],))
#     user = cursor.fetchone()

#     if request.method == 'POST':
#         new_password = generate_password_hash(request.form['password'])
#         cursor.execute("UPDATE user SET password=%s WHERE id=%s", (new_password, session['user_id']))
#         db.commit()
#         flash("Profile updated successfully!", "success")

#     return render_template('profile.html', user=user)

# # Reports Route
# @app.route('/reports')
# def reports():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     cursor.execute("SELECT SUM(rent) FROM apartments WHERE status='occupied'")
#     total_income = cursor.fetchone()[0]
#     return render_template('reports.html', total_income=total_income)

# #Admin Management Route
# @app.route('/admin_manage')
# def admin_manage():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('admin_manage.html')

# @app.route('/system_settings')
# def system_settings():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('system_settings.html')

# if __name__ == '__main__':
#     app.run(debug=True)



import datetime
import re
from flask import Flask, jsonify, make_response, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import connection
from werkzeug.security import generate_password_hash, check_password_hash
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import g
import mysql.connector
from config import db_config
from datetime import datetime
from mysql.connector import connect


# Initialize MySQL connection
connection = connect(
    host="localhost",
    user="root",
    password="Het@1305",
    database="flask_app"
)

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Het@1305",
    database="flask_app"
)
cursor = db.cursor()


def get_db_connection():
    if 'db_connection' not in g:
        g.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Het@1305",
            database="flask_app"
        )
    return g.db_connection

# Helper functions for OTP generation and sending email
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    try:
        sender_email = "hetkothari2005@gmail.com"  # Your Gmail address
        sender_password = "hgbh nuvn zfcw mtsu"    # App password generated
        subject = "Your OTP for Password Reset"
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        body = f"Your OTP for password reset is: {otp}"
        message.attach(MIMEText(body, "plain"))

        # Use Gmail's SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        return True
    except Exception as e:
        print("Error sending OTP email:", e)
        return False

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']

            # Check if username already exists
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username already exists. Please choose a different username.", "danger")
                return redirect(url_for('register'))

            # Insert user data into the database
            cursor.execute("INSERT INTO user (username, password, email, first_name, last_name, age) VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, password, email, first_name, last_name, age))
            db.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print("Error during registration:", e)
            flash("An error occurred. Please try again later.", "danger")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Use a new cursor for each query
            login_cursor = db.cursor()
            login_cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
            user = login_cursor.fetchone()
            login_cursor.close()  # Close cursor after use

            # Check if user exists and validate password
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password.", "danger")

        except mysql.connector.Error as err:
            print(f"Error: {err}")  # Print the error for debugging
            flash("An error occurred while trying to log in.", "danger")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    tenant_id=1
    apartment_id = session.get('apartment_id')
    apartment = get_apartment(apartment_id) 
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',apartment=apartment, tenant_id=tenant_id)

def get_apartment(apartment_id):
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM apartments WHERE apartment_id = %s", (apartment_id,))
    apartment = cursor.fetchone()
    cursor.close()
    return apartment

@app.teardown_appcontext
def close_db_connection(exception):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))


# Forgot password routes
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Initialize a new cursor with buffering to avoid unread result errors
        cursor = connection.cursor(buffered=True)
        
        try:
            cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
            user = cursor.fetchall()  # Fetch results to avoid unread result errors
            
            if user:
                otp = generate_otp()
                session['otp'] = otp
                session['email'] = email

                if send_otp(email, otp):
                    flash("OTP has been sent to your email.", "success")
                    return redirect(url_for('verify_otp'))
                else:
                    flash("Failed to send OTP. Please try again.", "danger")
            else:
                flash("Email not found.", "danger")
        
        finally:
            cursor.close()  # Ensure the cursor is closed after operation

    return render_template('forgot_password.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp_entered = request.form['otp']
        if otp_entered == session.get('otp'):
            flash("OTP verified. You can reset your password.", "success")
            return redirect(url_for('reset_password'))
        else:
            flash("Invalid OTP. Please try again.", "danger")
    return render_template('verify_otp.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if 'email' not in session:

        return redirect(url_for('login'))
        
    if request.method == 'POST':
        new_password = generate_password_hash(request.form['password'])
        email = session['email']
        
        cursor.execute("UPDATE user SET password=%s WHERE email=%s", (new_password, email))
        db.commit()

         # Clear session after password reset
        session.pop('email', None)
        session.pop('otp', None)

        flash("Your password has been reset successfully. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/apartments', methods=['GET', 'POST'])
def apartments():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Add a new apartment
        number = request.form['number']
        status = request.form['status']
        rent = request.form['rent']
        
        cursor.execute(
            "INSERT INTO apartments (number, status, rent) VALUES (%s, %s, %s)",
            (number, status, rent)
        )
        conn.commit()

    # Retrieve apartments
    cursor.execute("SELECT * FROM apartments")
    apartments = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('apartments.html', apartments=apartments)

@app.route('/add_apartment', methods=['GET', 'POST'])
def add_apartment():
    cursor = None  # Initialize cursor to None
    conn = None  # Initialize conn to None
    if request.method == 'POST':
        apartment_name = request.form['apartment_name']
        apartment_location = request.form['apartment_location']
        apartment_price = request.form['apartment_price']

        # Validate form input
        if not apartment_name or not apartment_location or not apartment_price:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_apartment'))

        try:
            # Establish database connection
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # Insert the new apartment
            cursor.execute("INSERT INTO apartments (name, location, price) VALUES (%s, %s, %s)",
                           (apartment_name, apartment_location, apartment_price))
            conn.commit()
            flash('Apartment added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
        finally:
            # Close the cursor and connection safely
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    return render_template('add_apartment.html')

# Route to handle printing a report for a tenant
@app.route('/print_report', methods=['POST'])
def print_report():
    tenant_id = request.form['tenant_id']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT t.name, p.status, p.method FROM tenants t JOIN payments p ON t.id = p.tenant_id WHERE t.id = %s", (tenant_id,))
    tenant_info = cursor.fetchone()

    cursor.close()
    conn.close()

    if tenant_info:
        # Generate PDF report
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)

        tenant_name, payment_status, payment_method = tenant_info
        pdf.drawString(100, 750, f"Tenant Report for {tenant_name}")
        pdf.drawString(100, 730, f"Payment Status: {payment_status}")
        pdf.drawString(100, 710, f"Payment Method: {payment_method}")

        pdf.showPage()
        pdf.save()

        pdf_buffer.seek(0)

        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={tenant_name}_Report.pdf'
        return response
    else:
        return "No report found for the specified tenant."

# Route to display specific apartment reports (with a unique endpoint name)
@app.route('/view_reports/<int:apartment_id>', endpoint='view_reports')
def view_reports(apartment_id):
    # Display apartment reports logic (can be customized as needed)
    return f"Reports for Apartment ID: {apartment_id}"


# Maintenance Requests Routes
@app.route("/maintenance_requests", methods=["GET", "POST"])
def maintenance_requests():
    cursor = db.cursor()

    if request.method == "POST":
        tenant_id = request.form["tenant_id"]
        apartment_id = request.form["apartment_id"]
        request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = request.form["description"]
        status = request.form["status"]

        # Insert new maintenance request into the database
        cursor.execute(
            "INSERT INTO maintenance_requests (tenant_id, apartment_id, request_date, description, status) VALUES (%s, %s, %s, %s, %s)",
            (tenant_id, apartment_id, request_date, description, status)
        )
        db.commit()

        return redirect(url_for("maintenance_requests"))

    # Retrieve maintenance requests from the database
    cursor.execute("SELECT request_id, description, status FROM maintenance_requests")
    requests = cursor.fetchall()
    cursor.close()

    return render_template("maintenance_requests.html", requests=requests)
# Profile Management Route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM user WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        new_password = generate_password_hash(request.form['password'])
        cursor.execute("UPDATE user SET password=%s WHERE id=%s", (new_password, session['user_id']))
        db.commit()
        flash("Profile updated successfully!", "success")

    return render_template('profile.html', user=user)

# Reports Route
@app.route('/reports', methods=['GET'])
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT SUM(rent) FROM apartments WHERE status='occupied'")
    total_income = cursor.fetchone()[0]
    return render_template('reports.html')

# Admin Management Route
@app.route('/admin_manage')
def admin_manage():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('admin_manage.html')

@app.route('/system_settings')
def system_settings():
    return render_template('system_settings.html')

def is_valid_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone) is not None

@app.route("/tenants", methods=["GET", "POST"])
def manage_tenants():
    cursor = db.cursor()

    if request.method == "POST":
        tenant_name = request.form["tenant_name"]
        apartment_id = request.form["apartment_number"]
        lease_start_date = request.form["lease_start_date"]
        lease_end_date = request.form["lease_end_date"]
        contact_info = request.form["contact_info"]
        email = request.form["email"]
        username = request.form["username"]
        raw_password = request.form["password"]
        
        # Validate phone number
        if not is_valid_phone(contact_info):
            return "Invalid phone number format. Please enter a valid number."

         # Hash the password
        hashed_password = generate_password_hash(raw_password)

        # Insert new tenant into the database
        cursor.execute("""
            INSERT INTO tenant (name, apartment_id, lease_start_date, lease_end_date, contact_info, email, username, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (tenant_name, apartment_id, lease_start_date, lease_end_date, contact_info, email, username, hashed_password))
        
        db.commit()

        return redirect(url_for("manage_tenants"))

    # Retrieve current tenants
    cursor.execute("SELECT * FROM tenant")
    tenants = cursor.fetchall()
    cursor.close()


    return render_template("tenants.html", tenants=tenants)




@app.route('/payment/<int:tenant_id>', methods=['GET'])
def payment(tenant_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email, username FROM tenant WHERE tenant_id = %s", (tenant_id,))
    tenant = cursor.fetchone()
    conn.close()
    return render_template('payment.html', tenant=tenant)

@app.route("/process_payment", methods=["POST"])
def process_payment():
    cursor = db.cursor()

    # Print the incoming form data for debugging
    print(request.form)

    # Get payment details from the request
    tenant_id = request.form.get("tenant_id")  # Retrieve tenant_id from the form data
    amount = request.form.get("amount")
    method = request.form.get("method")
    payment_date = request.form.get("payment_date")
    status = "pending"
    # Ensure tenant_id is present
    if not tenant_id:
        return "Error: Tenant ID is required for processing payments.", 400

    try:
        # Insert payment record into the database
        cursor.execute("""
            INSERT INTO payment (tenant_id, amount, method, payment_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (tenant_id, amount, method, payment_date, status))
        
        db.commit()
        return redirect(url_for("view_payments"))
    
    except mysql.connector.Error as e:
        db.rollback()
        return f"Database error: {e}", 500

    # flash("Payment Successful", "success")
    # return redirect(url_for('payment_status', tenant_id=tenant_id))

@app.route("/view_payments")
def view_payments():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM payment")  # Adjust this query according to your table structure
    payment = cursor.fetchall()

        # Debug output to check payments retrieved
    print("Payments retrieved:", payment)
    
    return render_template("view_payments.html", payment=payment)

@app.route('/payment_status/<int:tenant_id>', methods=['GET'])
def payment_status(tenant_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE tenant_id = %s ORDER BY created_at DESC LIMIT 1", (tenant_id,))
    transaction = cursor.fetchone()
    conn.close()
    return render_template('payment_status.html', transaction=transaction)

if __name__ == '__main__':
    app.run(debug=True)
