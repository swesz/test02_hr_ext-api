from flask import request, jsonify
from hr_app import hr_app, db, bcrypt
from models import Employee, Payroll, TimeTracking, Benefits, LeaveRequest
from flask_jwt_extended import create_access_token, jwt_required

# ------------------------ Employee Management ------------------------

# Register Employee
@hr_app.route('/register', methods=['POST'])
def register_employee():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_employee = Employee(
        name=data['name'], 
        email=data['email'], 
        job_title=data['job_title'], 
        department=data['department'], 
        salary=data['salary'],
        password_hash=hashed_password
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee registered successfully!"})

# Login (retrieve jwt access token)
@hr_app.route('/login', methods=['POST'])
def login():
    data = request.json
    employee = Employee.query.filter_by(email=data['email']).first()
    if employee and bcrypt.check_password_hash(employee.password_hash, data['password']):
        access_token = create_access_token(identity="employee.id") #"" to solve token error
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

# Get All Employees
@hr_app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    return jsonify([{"id": emp.id, "name": emp.name, "email": emp.email, "job_title": emp.job_title, "department": emp.department, "salary": emp.salary} for emp in employees])

# Get a Single Employee
@hr_app.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"id": employee.id, "name": employee.name, "email": employee.email, "job_title": employee.job_title, "department": employee.department, "salary": employee.salary})

# Update Employee
@hr_app.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
def update_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.json
    employee.name = data.get('name', employee.name)
    employee.job_title = data.get('job_title', employee.job_title)
    employee.salary = data.get('salary', employee.salary)
    employee.department = data.get('department', employee.department)

    db.session.commit()
    return jsonify({"message": "Employee updated successfully", "updated_employee": {
        "id": employee.id, "name": employee.name, "email": employee.email, "department": employee.department
    }})

# Delete Employee
@hr_app.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"})

# ------------------------ Leave Requests ------------------------

# Get All Leave Requests
@hr_app.route('/leave-requests', methods=['GET'])
@jwt_required()
def get_leave_requests():
    leave_requests = LeaveRequest.query.all()
    return jsonify([{"id": lr.id, "employee_id": lr.employee_id, "leave_type": lr.leave_type, "start_date": lr.start_date, "end_date": lr.end_date, "status": lr.status} for lr in leave_requests])

# Get Leave Requests by Employee ID
@hr_app.route('/leave-requests/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_leave_requests_by_employee(employee_id):
    leave_requests = LeaveRequest.query.filter_by(employee_id=employee_id).all()
    return jsonify([{"id": lr.id, "leave_type": lr.leave_type, "start_date": lr.start_date, "end_date": lr.end_date, "status": lr.status} for lr in leave_requests])

from datetime import datetime

# Request Leave (Fix for Date Conversion)
@hr_app.route('/leave-request', methods=['POST'])
@jwt_required()
def request_leave():
    data = request.json
    
    # Convert start_date and end_date from string to Python date object
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
    
    new_request = LeaveRequest(
        employee_id=data['employee_id'],
        leave_type=data['leave_type'],
        start_date=start_date,
        end_date=end_date
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    return jsonify({"message": "Leave request submitted!"})

# Update Leave Request
@hr_app.route('/leave-request/<int:id>', methods=['PUT'])
@jwt_required()
def update_leave_request(id):
    leave_request = LeaveRequest.query.get(id)
    if not leave_request:
        return jsonify({"error": "Leave request not found"}), 404

    data = request.json
    leave_request.leave_type = data.get('leave_type', leave_request.leave_type)
    leave_request.start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    leave_request.end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
    leave_request.status = data.get('status', leave_request.status)

    db.session.commit()
    return jsonify({"message": "Leave request updated successfully"})

# Delete Leave Request
@hr_app.route('/leave-request/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_leave_request(id):
    leave_request = LeaveRequest.query.get(id)
    if not leave_request:
        return jsonify({"error": "Leave request not found"}), 404

    db.session.delete(leave_request)
    db.session.commit()
    return jsonify({"message": "Leave request deleted successfully"})

# ------------------------ Payroll Management ------------------------

# Get All Payroll Records
@hr_app.route('/payroll', methods=['GET'])
@jwt_required()
def get_payroll_records():
    payroll_records = Payroll.query.all()
    return jsonify([{"id": p.id, "employee_id": p.employee_id, "gross_salary": p.gross_salary, "tax_deductions": p.tax_deductions, "net_salary": p.net_salary} for p in payroll_records])

# Get Payroll by Employee ID
@hr_app.route('/payroll/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_payroll_by_employee(employee_id):
    payroll = Payroll.query.filter_by(employee_id=employee_id).first()
    if not payroll:
        return jsonify({"error": "Payroll record not found"}), 404
    return jsonify({"id": payroll.id, "employee_id": payroll.employee_id, "gross_salary": payroll.gross_salary, "tax_deductions": payroll.tax_deductions, "net_salary": payroll.net_salary})

# Create Payroll Record (Simplified)
@hr_app.route('/payroll', methods=['POST'])
@jwt_required()
def create_payroll():
    data = request.json
    new_payroll = Payroll(
        employee_id=data['employee_id'],
        gross_salary=data['gross_salary'],
        tax_deductions=data['tax_deductions'],
        net_salary=data['gross_salary'] - data['tax_deductions']
    )
    db.session.add(new_payroll)
    db.session.commit()
    return jsonify({"message": "Payroll record created!"})

# Process Payroll
@hr_app.route('/process-payroll', methods=['POST'])
@jwt_required()
def process_payroll():
    data = request.json
    payroll = Payroll.query.filter_by(employee_id=data['employee_id']).first()
    if payroll:
        payroll.net_salary = payroll.gross_salary - payroll.tax_deductions
        db.session.commit()
        return jsonify({"message": "Payroll updated!"})
    return jsonify({"error": "Employee not found"}), 404

# Update Payroll
@hr_app.route('/payroll/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_payroll(employee_id):
    payroll = Payroll.query.filter_by(employee_id=employee_id).first()
    if not payroll:
        return jsonify({"error": "Payroll record not found"}), 404

    data = request.json
    payroll.gross_salary = data.get('gross_salary', payroll.gross_salary)
    payroll.tax_deductions = data.get('tax_deductions', payroll.tax_deductions)
    payroll.net_salary = payroll.gross_salary - payroll.tax_deductions

    db.session.commit()
    return jsonify({"message": "Payroll updated successfully"})

# Delete Payroll Record
@hr_app.route('/payroll/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_payroll(employee_id):
    payroll = Payroll.query.filter_by(employee_id=employee_id).first()
    if not payroll:
        return jsonify({"error": "Payroll record not found"}), 404

    db.session.delete(payroll)
    db.session.commit()
    return jsonify({"message": "Payroll record deleted successfully"})

# ------------------------ Time Tracking ------------------------

# Clock In
@hr_app.route('/time-tracking/clock-in', methods=['POST'])
@jwt_required()
def clock_in():
    data = request.json
    new_entry = TimeTracking(employee_id=data['employee_id'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Clock-in recorded successfully!"})

# Clock Out
@hr_app.route('/time-tracking/clock-out/<int:id>', methods=['PUT'])
@jwt_required()
def clock_out(id):
    time_entry = TimeTracking.query.get(id)
    if not time_entry:
        return jsonify({"error": "Time entry not found"}), 404

    data = request.json
    time_entry.hours_worked += data.get('hours_worked', 0)
    time_entry.overtime_hours += data.get('overtime_hours', 0)

    db.session.commit()
    return jsonify({"message": "Clock-out recorded successfully!"})

# Get Time Tracking Records
@hr_app.route('/time-tracking', methods=['GET'])
@jwt_required()
def get_time_tracking():
    records = TimeTracking.query.all()
    return jsonify([{"id": t.id, "employee_id": t.employee_id, "hours_worked": t.hours_worked, "overtime_hours": t.overtime_hours} for t in records])

# ------------------------ Employee Benefits ------------------------

# Get All Benefits
@hr_app.route('/benefits', methods=['GET'])
@jwt_required()
def get_benefits():
    benefits = Benefits.query.all()
    return jsonify([{"id": b.id, "employee_id": b.employee_id, "health_insurance": b.health_insurance, "retirement_plan": b.retirement_plan, "vacation_days": b.vacation_days} for b in benefits])

# Get Benefits by Employee ID
@hr_app.route('/benefits/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_benefits_by_employee(employee_id):
    benefits = Benefits.query.filter_by(employee_id=employee_id).first()
    if not benefits:
        return jsonify({"error": "Benefits record not found"}), 404
    return jsonify({"id": benefits.id, "employee_id": benefits.employee_id, "health_insurance": benefits.health_insurance, "retirement_plan": benefits.retirement_plan, "vacation_days": benefits.vacation_days})

# Enroll in Benefits
@hr_app.route('/benefits', methods=['POST'])
@jwt_required()
def enroll_in_benefits():
    data = request.json
    new_benefits = Benefits(
        employee_id=data['employee_id'],
        health_insurance=data.get('health_insurance', False),
        retirement_plan=data.get('retirement_plan', False),
        vacation_days=data.get('vacation_days', 0)
    )
    db.session.add(new_benefits)
    db.session.commit()
    return jsonify({"message": "Benefits enrollment successful!"})

# Update Benefits
@hr_app.route('/benefits/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_benefits(employee_id):
    benefits = Benefits.query.filter_by(employee_id=employee_id).first()
    if not benefits:
        return jsonify({"error": "Benefits record not found"}), 404

    data = request.json
    benefits.health_insurance = data.get('health_insurance', benefits.health_insurance)
    benefits.retirement_plan = data.get('retirement_plan', benefits.retirement_plan)
    benefits.vacation_days = data.get('vacation_days', benefits.vacation_days)

    db.session.commit()
    return jsonify({"message": "Benefits updated successfully!"})

# Remove Benefits
@hr_app.route('/benefits/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def remove_benefits(employee_id):
    benefits = Benefits.query.filter_by(employee_id=employee_id).first()
    if not benefits:
        return jsonify({"error": "Benefits record not found"}), 404

    db.session.delete(benefits)
    db.session.commit()
    return jsonify({"message": "Benefits removed successfully!"})
