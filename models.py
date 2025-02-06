from hr_app import hr_app, db  # Import both the Flask app and the database

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # For login

# Payroll Model
class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    gross_salary = db.Column(db.Float, nullable=False)
    tax_deductions = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)

# Time Tracking Model
class TimeTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    hours_worked = db.Column(db.Float, default=0)
    overtime_hours = db.Column(db.Float, default=0)

# Benefits Model
class Benefits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    health_insurance = db.Column(db.Boolean, default=False)
    retirement_plan = db.Column(db.Boolean, default=False)
    vacation_days = db.Column(db.Integer, default=0)

# Leave Requests Model
class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # Sick, Vacation
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending, Approved, Denied

with hr_app.app_context():
    db.create_all()