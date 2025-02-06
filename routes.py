from flask import request, jsonify
from hr_app import hr_app, db, bcrypt
from models import Employee, Payroll, TimeTracking, Benefits, LeaveRequest
from flask_jwt_extended import create_access_token, jwt_required

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

# Login
@hr_app.route('/login', methods=['POST'])
def login():
    data = request.json
    employee = Employee.query.filter_by(email=data['email']).first()
    if employee and bcrypt.check_password_hash(employee.password_hash, data['password']):
        access_token = create_access_token(identity="employee.id")
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

# Get All Employees (HR Only)
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

# Request Leave
@hr_app.route('/leave-request', methods=['POST'])
@jwt_required()
def request_leave():
    data = request.json
    new_request = LeaveRequest(
        employee_id=data['employee_id'],
        leave_type=data['leave_type'],
        start_date=data['start_date'],
        end_date=data['end_date']
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
    leave_request.start_date = data.get('start_date', leave_request.start_date)
    leave_request.end_date = data.get('end_date', leave_request.end_date)
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
