from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}

# EXAMPLE CODE FROM TEMPLATE

# @app.route("/about", methods=['POST'])
# def about():
#     return render_template('www.intellipaat.com')


# @app.route("/addemp", methods=['POST'])
# def AddEmp():
#     emp_id = request.form['emp_id']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     pri_skill = request.form['pri_skill']
#     location = request.form['location']
#     emp_image_file = request.files['emp_image_file']

#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

#     if emp_image_file.filename == "":
#         return "Please select a file"

#     try:

#         cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
#         db_conn.commit()
#         emp_name = "" + first_name + " " + last_name
#         # Uplaod image file in S3 #
#         emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
#         s3 = boto3.resource('s3')

#         try:
#             print("Data inserted in MySQL RDS... uploading image to S3...")
#             s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
#             bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
#             s3_location = (bucket_location['LocationConstraint'])

#             if s3_location is None:
#                 s3_location = ''
#             else:
#                 s3_location = '-' + s3_location

#             object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
#                 s3_location,
#                 custombucket,
#                 emp_image_file_name_in_s3)

#         except Exception as e:
#             return str(e)

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('AddEmpOutput.html', name=emp_name)





# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('HomePage.html')

# START CODING HERE

#------------------------------------------------------------------------------Student Sign Up
students = {}

# Redirect to student login page
@app.route('/toStudLogin')
def toLogin():
    return render_template('StudLogin.html')

# Redirect to student signup page
@app.route('/toStudSignUp')
def toSignup():
    return render_template('StudentSignUp.html')

@app.route('/studentsignup', methods=['POST'])
def student_signup():
    student_id = request.form.get('std_id')
    first_name = request.form.get('std_first_name')
    last_name = request.form.get('std_last_name')
    password = request.form.get('std_pass')
    confirm_password = request.form.get('confirm_std_pass')

    # Check if passwords match
    if password != confirm_password:
        return "Password confirmation does not match."

    # Store student data in the dictionary
    students[student_id] = {
        'first_name': first_name,
        'last_name': last_name,
        'password': password
    }
    insert_sql = "INSERT INTO studentInformation VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (student_id, first_name, last_name, password))
        db_conn.commit()
        std_name = "" + first_name + " " + last_name
    
    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('StudLogin.html')


#------------------------------------------------------------signin

# Student login function
@app.route('/studlogin', methods=['POST'])
def student_signin():
    # return render_template('StudLogin.html')
    student_id = request.form.get('std_lg_id')
    password = request.form.get('std_lg_pass')

    select_stmt = "SELECT std_password FROM studentInformation WHERE std_id = %(student_id)s"
    cursor = db_conn.cursor()
    dbPassword = cursor.execute(select_stmt, { (student_id)})


    # Check if the student exists in the dictionary (for demonstration purposes)
    if dbPassword == password:
        return f"Welcome, Student with ID {student_id}!"
    else:
        return "Invalid student ID or password."

    # return render_template('StudentHomePage.html')

    #     # Check if the student exists in the dictionary (for demonstration purposes)
    #     if student_id in students and students[student_id]['password'] == password:
    #         return f"Welcome, Student with ID {student_id}!"
    #     else:
    #         return "Invalid student ID or password."

    # return render_template('StudLogin.html')

#-----------------------------------------END OF STUDENT PAGE--------------------------------------------------------------


#-----------------------------------------COMPANY-----------------------------------------------------

# Company sign up
company = {}

# Redirect to company login page
@app.route('/toCompanyLogin')
def toComLogin():
    return render_template('CompanyLogin.html')

# Redirect to company register page
@app.route('/toCompanyRegister')
def toComRegister():
    return render_template('CompanyRegister.html')

@app.route("/companyRegis", methods=['POST'])
def comp_signup():
    company_id = request.form.get('comp_id')
    company_name = request.form.get('comp_name')
    company_industry = request.form.get('comp_industry')
    company_address = request.form.get('comp_address')
    company_password = request.form.get('comp_password')
    # company_confirm_password = request.form.get('comp_confirm_password')
    company_status = "Pending"

    # Check if password matches
    # if company_password !=company_confirm_password:
    #     return "Password does not match"
    
    # Store company data
    company[company_id] = { #rember to put = { }
        'company_name' : company_name,
        'company_industry' : company_industry,
        'company_address' : company_address,
        'company_password' : company_password, 
        'company_status' : company_status
    }

    insert_sql_comp = "INSERT INTO company VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql_comp, (company_id, company_name, company_industry, company_address, company_password, company_status))
        db_conn.commit()

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("Information has been uploaded...")
    print("Company {company_name} have signed up successfully!")
    return render_template('CompanyLogin.html')

# Company login function
@app.route('/companyLogin', methods=['GET'])
def comp_signin_page():

    cursor = db_conn.cursor()
    cursor.execute("SELECT comp_id, comp_name, comp_industry, comp_address, comp_password, comp_status FROM company")
    company = cursor.fetchall()
    cursor.close()

    company_log_id = request.args.get('company_id')
    company_log_password = request.args.get('company_password')
        
    if company_log_id and company_log_password:
        for row in company:
            if row[0] == company_log_id and row[4] == company_log_password:
                if row[5] == "Approved":
                    print ("Login successful")
                    return render_template('HomePage.html') #Testing
                else:
                    return "Account is not active"
    return (company_log_id)

#--------------------------------------------END OF COMPANY PAGE-----------------------------------

#--------------------------------------------STAFF-------------------------------------------------
staffInfo = {}

# Redirect to Staff HomePage
@app.route("/toStaffHomePage")
def toStaffHomePage():
    return render_template('StaffHomePage.html')

# Redirect to View Staff page
@app.route("/toViewStaff")
def toViewStaff():
    return render_template('ViewStaff.html')

# Redirect to Staff login page
@app.route("/toStaffLogin")
def toStaffLogin():
    return render_template('StaffLogin.html')

# Redirect to Staff register page
@app.route("/toStaffRegister")
def toStaffRegister():
    return render_template('StaffRegister.html')

# Redirect to Validate Company page
@app.route("/toValidateCompany")
def toValidateCompany():
    return render_template('ValidateCompany.html')

# Redirect to Assign Student to Supervisors page
@app.route("/toAssignStudents")
def toAssignStudents():
    return render_template('AssignStudents.html')

# to retrieve all staff data to view
@app.route('/get_staff', methods=['GET'])
def get_staff():
    try:
        # Execute the SQL query to retrieve stf_id and stf_name
        cursor = db_conn.cursor()        
        cursor.execute("SELECT stf_id, stf_name FROM staffInformation")
        staff_data = cursor.fetchall()

        # Define the list to hold the results
        staff_list = []

        # Iterate through the results and create a list of dictionaries
        for staff in staff_data:
            stf_id, stf_name = staff
            staff_list.append({
                'stf_id': stf_id,
                'stf_name': stf_name
            })

        # Serialize the data to JSON
        response_data = json.dumps(staff_list)

        # Create a JSON response
        response = Response(response=response_data, status=200, content_type='application/json')

        return response

    except Exception as e:
        error_message = {'error': str(e)}
        response_data = json.dumps(error_message)
        response = Response(response=response_data, status=500, content_type='application/json')
        return response
    
# to retrieve all supervisor data to view
@app.route('/get_supervisor', methods=['GET'])
def get_supervisor():
    try:
        # Execute the SQL query to retrieve supervisor data
        cursor = db_conn.cursor()        
        cursor.execute("SELECT spv_id, spv_name, spv_contact, spv_email, spv_subject FROM supervisorInformation")
        supervisor_data = cursor.fetchall()

        # Define the list to hold the results
        supervisor_list = []

        # Iterate through the results and create a list of dictionaries
        for supervisor in supervisor_data:
            spv_id, spv_name, spv_contact, spv_email, spv_subject = supervisor
            supervisor_list.append({
                'spv_id': spv_id,
                'spv_name': spv_name,
                'spv_contact': spv_contact,
                'spv_email': spv_email,
                'spv_subject': spv_subject                            
            })

        # Serialize the data to JSON
        response_data = json.dumps(supervisor_list)

        # Create a JSON response
        response = Response(response=response_data, status=200, content_type='application/json')

        return response

    except Exception as e:
        error_message = {'error': str(e)}
        response_data = json.dumps(error_message)
        response = Response(response=response_data, status=500, content_type='application/json')
        return response    

# to login as staff
@app.route('/stafflogin', methods=['GET'])
def staffLogin():
    # return render_template('StaffLogin.html')
    staff_id = request.form.get('stf_lg_id')
    staff_login_password = request.form.get('stf_lg_pass')

    select_stmt = "SELECT stf_pass FROM staffInformation WHERE stf_id = %(staff_id)s"
    cursor = db_conn.cursor()
    staff_db_Password = cursor.execute(select_stmt, { (staff_id)})


    # Check if the student exists in the dictionary (for demonstration purposes)
    if staff_db_Password == staff_login_password:
        return f"Welcome, Staff {staff_id}!"
    else:
        return "Invalid Staff ID or password."
    

# to register staff as staff
@app.route('/staffregister', methods=['POST'])
def staffregister():
    staff_reg_id = request.form.get('stf_register_id')
    staff_reg_name = request.form.get('stf_register_name')
    staff_reg_pass = request.form.get('stf_register_pass')
    staff_reg_confirm_pass = request.form.get('stf_register_confirm_pass')

    # Check if passwords match
    if staff_reg_pass != staff_reg_confirm_pass:
        return "Password does not match."

    # Store student data in the dictionary
    staffInfo[staff_reg_id] = {
        'stf_register_id': staff_reg_name,
        'stf_register_name': staff_reg_pass,

    }
    insert_sql = "INSERT INTO staffInformation VALUES (%s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (staff_reg_id, staff_reg_name, staff_reg_pass))
        db_conn.commit()
    
    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("Register successfully!")
    return render_template('StaffHomePage.html')

#--------------------------------------------END OF STAFF PAGE-------------------------------------

#--------------------------------------------SUPERVISOR--------------------------------------------

supervisorInfo = {}

# Redirect to View Supervisor page
@app.route("/toViewSupervisor")
def toViewSupervisor():
    return render_template('ViewSupervisor.html')

# Redirect to Supervisor login page
@app.route("/toSupervisorLogin")
def toSupervisorLogin():
    return render_template('SupervisorLogin.html')

# Redirect to Supervisor register page
@app.route("/toSupervisorRegister")
def toSupervisorRegister():
    return render_template('SupervisorRegister.html')

# to register supervisor as staff
@app.route('/supervisorregister', methods=['POST'])
def supervisorregister():
    supervisor_id = request.form.get('spv_id')
    supervisor_name = request.form.get('spv_name')
    supervisor_register_pass = request.form.get('spv_pass')
    supervisor_register_confirm_pass = request.form.get('confirm_spv_pass')
    supervisor_contact = request.form.get('spv_contact')
    supervisor_email = request.form.get('spv_email')
    supervisor_subject = request.form.get('spv_subject')    

    # Check if passwords match
    if supervisor_register_pass != supervisor_register_confirm_pass:
        return "Password does not match."

    # Store student data in the dictionary
    supervisorInfo[supervisor_id] = {
        'spv_name': supervisor_name,
        'spv_pass': supervisor_register_pass,
        'spv_contact': supervisor_contact,
        'spv_email': supervisor_email,
        'spv_subject': supervisor_subject
    }
    insert_sql = "INSERT INTO supervisorInformation VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (supervisor_id, supervisor_name, supervisor_register_pass, supervisor_contact, supervisor_email, supervisor_subject))
        db_conn.commit()
    
    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("Register successfully!")
    return render_template('StaffHomePage.html')


#--------------------------------------------END OF SUPERVISOR-------------------------------------

# END OF CODING
# Establish connection
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)