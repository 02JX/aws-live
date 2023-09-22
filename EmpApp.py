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

#Example code from template

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
    return render_template('StudentSignUp.html')

# START CODING HERE

#------------------------------------------------------------------------------Student Sign Up
students = {}

@app.route('/')
def index():
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

# Redirect from signup to login
@app.route('/StudLoginPage')
def toLogin():
    return render_template('StudLogin.html')

# Redirect from login to signup
@app.route('/toStudentSignUp')
def toSignup():
    return render_template('StudentSignUp.html')

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

#-------------------------------------------------------------------------------------------------------





# COMPANY PAGE
# Company sign up
company = {}

# Redirect to company register page
@app.route('/toCompanyRegister')
def toComRegister():
    return render_template('CompanyRegister.html')

# Redirect to company login page
@app.route('/toCompanyLogin')
def toComLogin():
    return render_template('CompanyLogin.html')

# Run company register function
# @app.route("/CompanyRegister", methods=['POST'])
# def company_signup():
#     company_id = request.form.get('comp_id')
#     company_name = request.form.get('comp_name')
#     company_industry = request.form.get('comp_industry')
#     company_password = request.form.get('comp_password')
#     company_confirm_password = request.form.get('comp_confirm_password')
#     company_address = request.form.get('comp_address')

#     # Check if password matches
#     if company_password !=company_confirm_password:
#         return "Password does not match"
    
#     # Store company data
#     company[company_id] {

#         'company_name' : company_name,
#         'company_industry' : company_industry,
#         'company_password' : company_password,
#         'company_address' : company_address
#     }

#     return f"Company {company_name} have signed up successfully!"

# Company login function
#@app.route("/CompanyLogin", methods=['POST'])
#def company_login():
    # Login function inside here

    #return










# END OF CODING
# Establish connection
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)