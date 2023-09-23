from flask import Flask, render_template, request, session, redirect
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

# Set a secret key for your Flask application
app.secret_key = 'never_gonna_give_you_up_never_gonna_let_you_down_never_gonna_run_around_and_hurt_you'  # Replace with a long and secure secret key

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

# Home page
@app.route("/toHomePage")
def toHome():
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
            if row[0] == company_log_id and row[4] == company_log_password: #If row starts at 1, it's actually 0 because Python :) 
                if row[5] == "Approved":
                    print ("Login successful")
                    session['company_id'] = company_log_id  # Store company_log_id in the session
                    return render_template('CompanyHome.html', company_log_id=company_log_id)
                else:
                    return "Account is not active"
    return "Your login details are not correct lol"

job = {}

@app.route('/jobPosting', methods=['GET', 'POST'])
def job_posting():
    # Retrieve company_log_id from the session
    company_log_id = session.get('company_id')

    # Initialize a flag to track whether the Company ID has been revealed
    show_company_id = False

    if request.method == 'POST':
        if 'reveal_id' in request.form:
            show_company_id = True

        elif 'submit_job' in request.form:
            job_id = request.form.get('job_id')
            job_name = request.form.get('job_name')
            job_description = request.form.get('job_desc')
            job_img = request.files.get('job_img')

            job[company_log_id] = { #rember to put = { }
                'job_id' : job_id,
                'job_name' : job_name,
                'job_description' : job_description,
            }

            insert_sql_comp = "INSERT INTO internship VALUES (%s, %s, %s, %s)"
            cursor = db_conn.cursor()

            if job_img.filename == "":
                return "ples selec file name lol"

            try:
                cursor.execute(insert_sql_comp, (company_log_id, job_id, job_name, job_description))
                db_conn.commit()
                # Upload image file in S3 
                job_img_in_s3 = str(company_log_id) + "_image_file"
                s3 = boto3.resource('s3')

                try:
                    print("Data inserted...Uploaded to S3")
                    s3.Bucket(custombucket).put_object(Key=job_img_in_s3, Body=job_img)
                    bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                    s3_location = (bucket_location['LocationConstraint'])

                    if s3_location is None:
                        s3_location = ''
                    else: 
                        s3_location = '-' + s3_location

                    object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    job_img_in_s3)


                except Exception as e:
                    return str(e)

            except Exception as e:
                return str(e)

            finally:
                cursor.close()

            return "Job posted successfully!"

    # Render the template and pass the company_log_id and show_company_id to it
    return render_template('CompanyHome.html', company_log_id=company_log_id, show_company_id=show_company_id)



#--------------------------------------------END OF COMPANY PAGE-----------------------------------

#--------------------------------------------STAFF-------------------------------------------------
staffInfo = {}

# Redirect to Staff HomePage
@app.route("/toStaffHomePage")
def toStaffHomePage():
    return render_template('StaffHomePage.html')

# Redirect to Staff login page
@app.route("/toStaffLogin")
def toStaffLogin():
    return render_template('StaffLogin.html')

@app.route("/toViewAssigned")
def toViewAssigned():
    return render_template('ViewAssign.html')

@app.route("/supervisorData")
def supervisorData():
    return render_template('DisplaySupervisors.html')

# Redirect to Staff register page
@app.route("/toStaffRegister")
def toStaffRegister():
    return render_template('StaffRegister.html')

# Redirect to Validate Company page
@app.route("/toValidateCompany")
def toValidateCompany():
    return render_template('ValidateCompany.html')

# Redirect to Assign Student to Supervisors page
@app.route("/toAssignStudent")
def toAssignStudents():
    return render_template('AssignStudents.html')
    
# Staff login function
@app.route('/stafflogin', methods=['GET'])
def staffLogin():

    cursor = db_conn.cursor()
    cursor.execute("SELECT stf_id, stf_name, staff_pass FROM staffInformation")
    staff = cursor.fetchall()
    cursor.close()

    staff_log_id = request.args.get('stf_id')
    staff_log_password = request.args.get('stf_password')
        
    if staff_log_id and staff_log_password:
        for row in staff:
            if row[0] == staff_log_id and row[2] == staff_log_password:
                print ("Login successful")
                return render_template('StaffHomePage.html')
            else:
                return "Incorrect login details"
    return (staff_log_id)    

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


# Display Supervisors
@app.route("/supervisorData", methods=['GET'])
def supervisor_data():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM supervisorInformation")
    supervisors = cursor.fetchall()
    print(supervisors)
    cursor.close()

    return render_template('DisplaySupervisors.html', supervisors=supervisors)


# Validate Company function
@app.route('/validateCompany', methods=['GET','POST'])
def validate_comp_page():

    cursor = db_conn.cursor()
    cursor.execute("SELECT comp_id, comp_name, comp_industry, comp_address, comp_password, comp_status FROM company WHERE comp_status = 'Pending'")
    companyDetails = cursor.fetchall()
    cursor.close()

        # Render the HTML template with the fetched data
    return render_template('ValidateCompany.html', pending_companies=companyDetails)

# View Student Assigned to SuperVisor
@app.route('/viewAssignedStudents', methods=['GET', 'POST'])
def viewAssignedStudents():

    cursor = db_conn.cursor()
    cursor.execute("SELECT spv_id, spv_name, spv_pass, spv_contact, spv_email, spv_subject FROM supervisorInformation")
    supervisor = cursor.fetchall()
    cursor.close()

    spv_id = request.args.get('spv_id')
        
    if spv_id:
        for row in supervisor:
            if row[0] == spv_id :
                    session['spv_id'] = spv_id  # Store staff_log_id in the session
                    return render_template('DisplayAssignedStudent.html', spv_id=spv_id)
            else:
                return "Account is not active"
    return "No related staff found"


supervisor = {}

@app.route('/displayAssignedStudent/<string:supervisor_name_display>', methods=['GET', 'POST'])
def displayAssignedStudent(supervisor_name_display):
    # Retrieve spv_id from the session
    supervisor_id = session.get('spv_id')

    cursor = db_conn.cursor()
    print(supervisor_id )
    cursor.execute("SELECT spv_id, spv_name, spv_pass, spv_contact, spv_email, spv_subject FROM supervisorInformation")
    supervisor = cursor.fetchall()
    cursor.close()

    # cursor = db_conn.cursor()
    # cursor.execute("SELECT comp_id, comp_name, comp_industry, comp_address, comp_password, comp_status FROM company")
    # company = cursor.fetchall()
    # cursor.close()

    for row in supervisor:
        if row[0] == supervisor_id:
            return render_template(spv_name=supervisor_name_display)
        else:
            return "Incorrect login details"
    return (supervisor_id)   


#--------------------------------------------END OF STAFF PAGE-------------------------------------

#--------------------------------------------SUPERVISOR--------------------------------------------

supervisorInfo = {}

# Redirect to Supervisor login page
@app.route("/toSupervisorLogin")
def toSupervisorLogin():
    return render_template('SupervisorLogin.html')

# Redirect to Supervisor register page
@app.route("/toSupervisorRegister")
def toSupervisorRegister():
    return render_template('SupervisorRegister.html')



# Redirect to Intern Application
@app.route("/toInternApplication")
def toInternApplication():
    return render_template('InternApplication.html')

# Redirect to PortFolioEricTan
@app.route("/toPortfolioEricTan")
def toPortfolioEricTan():
    return render_template('PortfolioEricTan.html')




# Supervisor login function
@app.route('/supervisorLogin', methods=['GET'])
def supervisorLogin():

    cursor = db_conn.cursor()
    cursor.execute("SELECT spv_id, spv_name, spv_pass, spv_contact, spv_email, spv_subject FROM supervisorInformation")
    supervisorInformation = cursor.fetchall()
    cursor.close()

    spv_id = request.args.get('spv_id')
    spv_pass = request.args.get('spv_pass')
        
    if spv_id and spv_pass:
        for row in supervisorInformation:
            if row[0] == spv_id and row[2] == spv_pass:
                print ("Login successful")
                return render_template('SupervisorHomePage.html')
            else:
                return "Incorrect login details"
    return (spv_id)    

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
    insert_sql = "INSERT INTO supervisorInformation VALUES (%s, %s, %s, %s, %s, %s)"
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

#--------------------------------------------PORTFOLIO---------------------------------------------
# Redirect to portfolio leejiaxuan
@app.route("/toPFLeeJiaXuan")
def toLJX():
    return render_template('PortfolioLeeJiaXuan.html')

# Redirect to portfolio tanjunchuan
@app.route("/toPFTanJunChuan")
def toTJC():
    return render_template('PortfolioTanJunChuan.html')

# Redirect to portfolio tamjiashun
@app.route("/toPFTamJiaShun")
def toTJS():
    return render_template('PortfolioTamJiaShun.html')

# Redirect to portfolio nguyenquanghien
@app.route("/toPFNguyenQuangHien")
def toNQH():
    return render_template('PortfolioNguyenQuangHien.html')

# Redirect to portfolio eric
@app.route("/toPFEricTan")
def toET():
    return render_template('PortfolioEricTan.html')

# END OF CODING
# Establish connection
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)