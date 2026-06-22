# Online Catering Management System - Flask Web Application

##  Project Overview

The Online Catering Management System is a web-based application developed using Flask that helps manage catering services efficiently. The system provides a platform where customers can interact with catering service providers, explore available services, and manage catering-related activities through an easy-to-use interface.

This project focuses on simplifying catering operations by providing features such as customer registration, service provider management, menu/item management, and booking-related functionalities.

---

##  Features

###  Customer Module
- Customer registration and login
- OTP-based email verification
- Customer profile management
- Search and explore catering services
- View available catering items and prices

###  Service Provider Module
- Service provider registration
- Provider authentication
- Manage catering items
- Update menu and pricing details
- Manage service-related information

###  Email Verification
- OTP generation and verification using email services
- Secure user verification process

###  Data Management
- Stores customer details
- Stores service provider details
- Maintains catering items and pricing information

---

##  Technologies Used

### Backend
- Python
- Flask

### Frontend
- HTML
- CSS
- JavaScript

### Data Storage
- CSV files

### Libraries
- Pandas
- SMTP (Email Service)
- Flask Sessions

---

##  Project Structure

```
online-catering-management-system

│── app.py
│── customers.csv
│── service_providers.csv
│── items_prices.csv
│── busy_dates.csv
│
├── templates/
│ ├── HTML pages
│
├── static/
│ ├── CSS
│ └── JavaScript
│
└── README.md

```

#  How to Run the Project

Follow these steps to run the application locally.

1. Clone the Repository
   ```bash
   git clone https://github.com/ShreyaRai03/online-catering-management-system.git
2. Navigate into the Project Folder
   ```bash
   cd online-catering-management-system
3. Create a Virtual Environment
   ```bash
   python -m venv venv
4. Activate Virtual Environment
   For Windows:
   ```bash
   venv\Scripts\activate
5. Install Required Dependencies
   ```bash
   pip install -r requirements.txt
6. Run the Flask Application
   ```bash
   python app.py
7. Open in Browser
   Open:
   http://127.0.0.1:5000/


### Project Objectives

- To digitize catering service management
- To simplify customer and catering provider interaction
- To reduce manual handling of catering information
- To provide an efficient platform for managing catering operations

###  Key Highlights
- Built a full-stack web application using Flask
- Implemented OTP-based email verification system
- Managed dynamic data using CSV-based storage
- Developed role-based modules for customers and service providers

### Future Enhancements
- Integration with MySQL database
- Online payment gateway
- Order tracking system
- Admin dashboard
- Cloud deployment
- Improved user interface

### Author
Shreya

Aspiring Software Engineer | Machine Learning Enthusiast | Python Developer

### If you like this project

Give it a ⭐ on GitHub and feel free to contribute or improve it!
