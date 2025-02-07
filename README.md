# test02_hr_ext-api
 Additional functionality
 
This project is a **Human Resources & Payroll REST API**, designed to mimic HR software functionality.

## Features
- Employee Registration & Authentication (JWT-based)  
- Payroll Processing & Tax Deduction Calculations  
- Time Tracking & Overtime Calculation  
- Leave Requests & Approval System  
- Benefit Enrollment (Health, Retirement Plans)  

## Technologies Used
- Python, Flask (Backend)
- SQLite + SQLAlchemy (Database)
- Marshmallow (Data serialization)
- JWT Authentication

## Files
- app.py (main app initializer:	starts Flask app, loads configurations, imports routes)
- models.py	(database structure: tables and relationships)
- routes.py	(handles API requests: endpoints for CRUD operations)

## How to Run
1. Clone this repository: 
git clone https://github.com/USERNAME/test02_hr_ext-api.git

2. Install dependencies: 
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy flask-bcrypt flask-jwt-extended

3. Start the API:
python hr_app.py

4. Use **Postman** to test API requests.

## API Endpoints
- Authentication & Employee Management

    **POST** `/register` – Register a new employee
    **POST** `/login` – Authenticate employee & get JWT token for Admin access
    **GET** `/employees` – Retrieve employee list
    **GET** `/employees/<id>` – Retrieve a single employee by ID
    **PUT** `/employees/<id>` – Update an existing employee by ID
    **DELETE** `/employees/<id>` – Delete an employee by ID

- Payroll Management 

    **POST** `/payroll` – Create an initial payroll record for an employee
    **GET** `/payroll` – Retrieve all payroll records (Admin only)
    **GET** `/payroll/<employee_id>` – Retrieve payroll details for a specific employee
    **PUT** `/payroll/<employee_id>` – Update payroll details (gross salary, tax deductions, etc.)
    **DELETE** `/payroll/<employee_id>` – Delete a payroll record
    **POST** `/process-payroll` – Calculate and update the net salary for an employee

- Leave Requests

    **POST** `/leave-request` – Submit a leave request
    **GET** `/leave-requests` – Retrieve all leave requests (Admin only)
    **GET** `/leave-requests/<employee_id>` – Retrieve leave requests for a specific employee
    **PUT** `/leave-request/<id>` – Update an existing leave request (e.g., change status to "Approved")
    **DELETE** `/leave-request/<id>` – delete a leave request

- Time Tracking

    **POST** `/time-tracking/clock-in` – Clock in an employee (record work start time)
    **PUT** `/time-tracking/clock-out/<id>` – Clock out an employee and update hours worked
    **GET** `/time-tracking` – Retrieve all time tracking records

- Employee Benefits

    **POST** `/benefits` – Enroll an employee in benefits (health insurance, retirement, vacation days)
    **GET** `/benefits` – Retrieve all benefits records (Admin only)
    **GET** `/benefits/<employee_id>` – Retrieve benefits for a specific employee
    **PUT** `/benefits/<employee_id>` – Update an employee's benefits (modify health, retirement, or vacation days)
    **DELETE** `/benefits/<employee_id>` – Remove an employee's benefits


## License
MIT License
