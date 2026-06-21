import csv
import smtplib
import random
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Helper functions
def send_otp(email):
    """Send OTP to the given email."""
    otp = random.randint(100000, 999999)
    try:
        # Email configuration
        sender_email = os.getenv("SENDER_EMAIL", "dscatreeing@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD", "lszl urfy lhlm vshz")

        # Create email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "Your OTP for Catering Management System"
        message.attach(MIMEText(f"Your OTP is {otp}", "plain"))

        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("OTP sent successfully.")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
    return otp

def write_to_csv(filename, data, headers=None):
    """Write data to a CSV file."""
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists and headers:
            writer.writerow(headers)
        writer.writerow(data)

def read_csv(filename):
    """Read data from a CSV file."""
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)

# Routes for Service Provider Management
@app.route('/signup/service_provider', methods=['GET', 'POST'])
def service_provider_signup():
    if request.method == 'POST':
        email = request.form['email']
        otp = send_otp(email)
        session['otp'] = otp
        session['signup_email'] = email
        flash("OTP sent to your email. Please verify.")
        return redirect(url_for('verify_otp', user_type='service_provider'))
    return render_template('service_provider_signup.html')
@app.route('/update_items', methods=['GET', 'POST'])
def update_service_provider_items():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        service_providers = read_csv("service_providers.csv")

        for provider in service_providers:
            if provider[0] == email and provider[1] == password:
                area = provider[4]
                print(f"Welcome, {provider[2]}")

                try:
                    df = pd.read_csv("veg.csv")
                    if 'Item' not in df.columns:
                        flash("The 'veg.csv' file does not have an 'Item' column.")
                        return redirect(url_for('update_service_provider_items'))

                    # Define the column name once the provider is authenticated
                    column_name = f"{provider[2]}_{area}"

                    # Prepare list of items and their current rates
                    items = [{'name': item, 'rate': df.loc[df['Item'] == item, column_name].iloc[0] if column_name in df.columns else 0}
                             for item in df['Item']]

                    # Check and update rates from the form
                    rates = {}
                    for item in df['Item']:
                        rate = request.form.get(f"rate_{item}")
                        if rate:
                            try:
                                rates[item] = float(rate)
                            except ValueError:
                                flash(f"Invalid rate for item: {item}")
                                return redirect(url_for('update_service_provider_items'))

                    # If rates were provided, update the CSV
                    if rates:
                        for item, rate in rates.items():
                            df.loc[df['Item'] == item, column_name] = rate

                        df.to_csv("veg.csv", index=False)
                        flash("Item rates updated successfully.")
                        return redirect(url_for('update_service_provider_items'))

                except FileNotFoundError:
                    flash("The file 'veg.csv' was not found.")
                    return redirect(url_for('update_service_provider_items'))

        flash("Invalid email or password.")
    else:
        items = []
        # Retrieve items and rates to display
        try:
            df = pd.read_csv("veg.csv")
            if 'Item' in df.columns:
                items = [{'name': item, 'rate': 0} for item in df['Item']]  # Set a default rate of 0 for items
        except FileNotFoundError:
            flash("The file 'veg.csv' was not found.")
        
    return render_template('update_service_provider_items.html', items=items)

@app.route('/update_busy_dates', methods=['GET', 'POST'])
def update_busy_dates():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        service_providers = read_csv("service_providers.csv")

        for provider in service_providers:
            if provider[0] == email and provider[1] == password:
                busy_dates = request.form['busy_dates'].split(',')
                busy_dates = [date.strip() for date in busy_dates]
                write_to_csv("busy_dates.csv", [email] + busy_dates,
                             headers=["Email"] + [f"BusyDate_{i+1}" for i in range(len(busy_dates))])
                flash("Busy dates updated successfully.")
                return redirect(url_for('update_busy_dates'))

        flash("Invalid email or password.")
    return render_template('update_busy_dates.html')

# Routes for Customer Management
@app.route('/signup/customer', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        email = request.form['email']
        otp = send_otp(email)
        session['otp'] = otp
        session['signup_email'] = email
        flash("OTP sent to your email. Please verify.")
        return redirect(url_for('verify_otp', user_type='customer'))
    return render_template('customer_signup.html')


@app.route('/verify_otp/<user_type>', methods=['GET', 'POST'])
def verify_otp(user_type):
    if request.method == 'POST':
        # Check for OTP and form fields
        entered_otp = request.form.get('otp')  # This should match the name attribute in the form
        entered_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Ensure OTP matches the session value
        if not entered_otp or not entered_password or not confirm_password:
            flash("All fields are required.")
            return redirect(request.url)  # Redirect back to the form if any field is missing

        try:
            if int(entered_otp) == session.get('otp'):
                # Handle password and other data
                if entered_password != confirm_password:
                    flash("Passwords do not match.")
                    return redirect(request.url)

                email = session.get('signup_email')
                if user_type == 'service_provider':
                    # Handle service provider signup
                    username = request.form['username']
                    phone = request.form['phone']
                    area = request.form['area']
                    write_to_csv("service_providers.csv", [email, entered_password, username, phone, area],
                                 headers=["Email", "Password", "Username", "Phone", "Area"])
                    flash("Service provider signup successful.")
                elif user_type == 'customer':
                    # Handle customer signup
                    username = request.form['username']
                    area = request.form['area']
                    write_to_csv("customers.csv", [email, entered_password, username, area],
                                 headers=["Email", "Password", "Username", "Area"])
                    flash("Customer signup successful.")

                return redirect(url_for('index'))
            else:
                flash("Invalid OTP. Please try again.")
        except Exception as e:
            flash(f"Error processing OTP: {e}")
            return redirect(request.url)

    return render_template('verify_otp.html', user_type=user_type)
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        # Step 1: Customer Login and Area Selection
        if 'find_providers' in request.form:
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            area = request.form['area'].strip()

            # Verify customer credentials
            customers = read_csv("customers.csv")
            customer = next((c for c in customers if c[0] == email and c[1] == password), None)

            if not customer:
                flash("Invalid email or password.")
                return redirect(url_for('place_order'))

            # Fetch available service providers
            service_providers = read_csv("service_providers.csv")
            available_providers = [sp for sp in service_providers if sp[4].lower() == area.lower()]

            if not available_providers:
                flash(f"No service providers found in {area}.")
                return redirect(url_for('place_order'))

            # Save to session
            session['email'] = email
            session['area'] = area
            session['available_providers'] = available_providers
            return render_template('place_order.html', available_providers=available_providers)

        # Step 2: Service Provider Selection
        if 'select_provider' in request.form:
            provider_choice = int(request.form['provider_choice']) - 1
            available_providers = session.get('available_providers', [])

            if not available_providers or provider_choice < 0 or provider_choice >= len(available_providers):
                flash("Invalid provider selection.")
                return redirect(url_for('place_order'))

            selected_provider = available_providers[provider_choice]
            provider_name_area = f"{selected_provider[2]}_{session['area']}"

            # Fetch provider's item pricing
            try:
                df = pd.read_csv("veg.csv")
                if provider_name_area not in df.columns:
                    flash(f"No pricing available for {selected_provider[2]} in {session['area']}.")
                    return redirect(url_for('place_order'))

                # Prepare order details
                order_details = [
                    {'name': row['Item'], 'rate': row[provider_name_area]}
                    for _, row in df.iterrows() if row[provider_name_area] > 0
                ]

                session['selected_provider'] = selected_provider
                session['order_details'] = order_details
                return render_template('place_order.html', order_details=order_details)
            except FileNotFoundError:
                flash("The 'veg.csv' file was not found.")
                return redirect(url_for('place_order'))

        # Step 3: Finalize Order
        if 'finalize_order' in request.form:
            quantities = {
                item['name']: int(request.form.get(f"quantity_{item['name']}", 0))
                for item in session.get('order_details', [])
            }

            # Calculate total cost
            total_cost = sum(
                item['rate'] * quantities[item['name']]
                for item in session['order_details'] if quantities[item['name']] > 0
            )

            # Prepare final order summary
            final_order_summary = [
                {'name': item['name'], 'quantity': quantities[item['name']], 'rate': item['rate']}
                for item in session['order_details'] if quantities[item['name']] > 0
            ]

            if not final_order_summary:
                flash("Please select at least one item to proceed with the order.")
                return redirect(url_for('place_order'))

            session['final_order_summary'] = final_order_summary
            session['total_cost'] = total_cost
            return render_template('place_order.html', final_order_summary=final_order_summary, total_cost=total_cost)

        # Step 4: Submit Order
        if 'submit_order' in request.form:
            address = request.form['address'].strip()
            date = request.form['date'].strip()
            final_order_summary = session.get('final_order_summary', [])
            total_cost = session.get('total_cost', 0)
            selected_provider = session.get('selected_provider')

            # Notify provider
            if selected_provider:
                notify_provider(selected_provider, final_order_summary, address, date)
                flash(f"Order placed successfully! Total cost: ₹{total_cost}")
                session.clear()  # Clear session after order
                return redirect(url_for('index'))

    return render_template('place_order.html')

def notify_provider(provider, order_details, address, date):
    """Send email to the service provider with order details."""
    email = provider[0]
    try:
        sender_email = os.getenv("SENDER_EMAIL", "dscatreeing@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD", "lszl urfy lhlm vshz")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "New Catering Order Notification"

        order_summary = "\n".join([f"{item['name']}: {item['quantity']} plates" for item in order_details])
        body = f"""
        Hello {provider[2]},
        
        You have a new catering order scheduled for {date}. Please find the details below:

        Delivery Address:
        {address}

        Order Details:
        {order_summary}

        Please contact the customer for any clarification or confirmation.

        Regards,
        Catering Management System
        """

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Provider notified successfully.")
    except Exception as e:
        print(f"Failed to notify provider: {e}")
# Home route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False)
