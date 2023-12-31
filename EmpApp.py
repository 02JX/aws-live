from flask import Flask, render_template, request, session, redirect, send_file
from pymysql import connections
import os
import boto3
import botocore
from io import BytesIO
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
# # Redirect index
# @app.route('/toIndex')
# def toIndex():
#     return render_template('index.html')

# Redirect index (signup)
@app.route('/toStdSignUp')
def toStdSignUp():
    return render_template('StudentSignUp.html')

# Redirect to login
@app.route('/toStudLogin')
def toStdLogin():
    return render_template('StudLogin.html')
    
# Redirect to StudentHomePage
@app.route('/toStdHomePage')
def toStdHomePage():
    return render_template('StudentHomePage.html')

# Redirect to StudentHomePage
@app.route('/toStdViewCompPage')
def toStdViewCompPage():
    return render_template('StudentViewCompany.html')

# Redirect to StudentHomePage
@app.route('/toStdViewProfilePage')
def toStdViewProfilePage():
    return render_template('StudentProfile.html')

    
#----------------------------------------------------------------------------global variable

student_id = ""
student_password = ""
std_company_id = ""
std_cmpDetails = ""
std_jobDetails = ""



#-----------------------------------------------------------------------------
#database route

@app.route('/studentsignup', methods=['GET', 'POST'])
def signup():
    global student_password
    student_id = request.form.get('std_id')
    first_name = request.form.get('std_first_name')
    last_name = request.form.get('std_last_name')
    student_password = request.form.get('std_pass')
    confirm_password = request.form.get('confirm_std_pass')


    # Check if passwords match
    if student_password != confirm_password:
        return "Password confirmation does not match."

    # Store student data in the dictionary
    students[student_id] = {
        'first_name': first_name,
        'last_name': last_name,
        'password': student_password
    }
    insert_sql = "INSERT INTO studentInformation VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (student_id, first_name, last_name, student_password, ""))
    db_conn.commit()
    cursor.close()

    return render_template('StudLogin.html')


#------------------------------------------------------------signin

# Student login function
@app.route('/studlogin', methods=['GET'])
def student_signin():

    

    cursor = db_conn.cursor()
    cursor.execute("SELECT std_id, std_pass FROM studentInformation")
    dbPassword = cursor.fetchall()
    cursor.close()

    student_id = request.args.get('std_lg_id')
    password = request.args.get('std_lg_pass')
    
  

    show_job = "SELECT comp_id, job_id, job_name, job_description FROM internship"
    cursor = db_conn.cursor()
    cursor.execute(show_job)
    jobName = cursor.fetchall()
    cursor.close()


    if student_id and password:
        for row in dbPassword:
            if row[0] == student_id and row[1] == password:
                # session['std_id'] = student_id  # Store student_id in the session for future uses
                session['student_id'] = student_id  
                return render_template('StudentHomePage.html', jobName = jobName, student_id = student_id)
        
        # If none of the rows matched, return an error message
        return "Wrong username or password"
    
    # If student_id or password is missing, return an error message
    return "Please provide both username and password"



    #------------------------StudentHome Page

    # Student home function
@app.route('/std_homepage', methods=['GET', 'POST'])
def std_home_page():
    student_id = session.get('student_id')
    std_company_id = request.form.get('cmp_id')
    session['std_company_id'] = std_company_id 
    

    search_cmp = "SELECT comp_name, comp_industry, comp_address FROM company WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (std_company_id))
    cmpdetails = cursor.fetchall()
    cursor.close()


    return render_template('StudentViewCompany.html', cmpdetails = cmpdetails, student_id = student_id, std_company_id = std_company_id)



        #------------------------Student View Company Page

    # Student apply intern function
@app.route('/stdapplyintern', methods=['GET', 'POST'])
def std_viewCompany():
    student_id = session.get('student_id')
    std_company_id = session.get('std_company_id')
  

    search_cmp = "SELECT comp_name FROM company WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (std_company_id))
    cmpName = cursor.fetchall()
    cursor.close()

    company_name = cmpName[0]
    intern_status = "pending"




    apply_intern = "INSERT INTO student VALUES (%s, %s, %s, %s ,%s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(apply_intern, (student_id, std_company_id, company_name, intern_status, "", ""))
    db_conn.commit()
    cursor.close()


    

    return "You are succeessful to apply!"

            #------------------------Student View Profile Page

    # Student View Profile function
@app.route('/viewProfile', methods=['GET', 'POST'])
def std_viewProfile():
    student_id = session.get('student_id')

    std_company_id = session.get('std_company_id')


    search_std_name = "SELECT std_first_name, std_last_name FROM studentInformation WHERE std_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_std_name, (student_id))
    stdInfor = cursor.fetchall()
    cursor.close()

    

    search_cmp = "SELECT cmp_name, intern_status FROM student WHERE std_id =%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (student_id))
    cmpName = cursor.fetchall()
    cursor.close()

    return render_template('StudentProfile.html', stdInfor = stdInfor, student_id = student_id, cmpName = cmpName, std_company_id = std_company_id)


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

# Redirect to company home page
@app.route('/toCompanyHomePage')
def toCompanyHome():
    company_log_id = session.get('company_id')
    return render_template('CompanyHome.html', company_log_id=company_log_id)


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

    # Check if the company ID already exists in the database
    select_sql_comp = "SELECT * FROM company WHERE comp_id = %s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql_comp, (company_id,))
        existing_company = cursor.fetchone()

        if existing_company:
            return render_template('CompanyRegister.html', error_message="Company ID already exists. Please choose a different ID.")

        # If the company ID is unique, proceed with registration
        insert_sql_comp = "INSERT INTO company VALUES (%s, %s, %s, %s, %s, %s)"
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
                    return render_template('CompanyLogin.html', error_message="Your Company account has not been activated! Please contact Admin")
    return render_template('CompanyLogin.html', error_message="Wrong Login Details or No Accounts With Such Details")


# View Company Details
@app.route('/toViewCompanyDetails', methods=['GET'])
def view_company_details():
    # Check if the user is logged in as a company
    if 'company_id' in session:
        company_id = session['company_id']

        cursor = db_conn.cursor()
        cursor.execute("SELECT comp_id, comp_name, comp_industry, comp_address, comp_status FROM company WHERE comp_id = %s", (company_id,))
        company = cursor.fetchone()  # Assuming comp_id is unique
        cursor.close()

        if company:
            # Render the CompanyDetails.html template with company details
            return render_template('CompanyDetails.html', company=company)
    
    # If not logged in or company not found, redirect to login page
    return render_template('CompanyLogin.html', error_message="Please log in to view company details")

job = {}

# Redirect to company job posting page
@app.route('/toJobPosting')
def toJobPosting():
    company_log_id = session.get('company_id')
    return render_template('CompanyJobPosts.html', company_log_id=company_log_id)

# # Redirect to company view job post page
# @app.route('/toViewJobs')
# def toViewJobs():
#     company_log_id = session.get('company_id')
#     return render_template('CompanyViewJobs.html', company_log_id=company_log_id)

@app.route('/toViewJobs', methods=['GET'])
def comp_view_job_page():
    company_log_id = session.get('company_id')

    cursor = db_conn.cursor()

    # Modify the SQL query to filter by comp_id
    sql_query = "SELECT comp_id, job_id, job_name, job_description, job_status, job_file_name FROM internship WHERE comp_id = %s"
    cursor.execute(sql_query, (company_log_id,))

    company_job_data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyViewJobs.html', company_log_id=company_log_id, company_job_data=company_job_data)

# Filter Job Status
@app.route('/filterJobStatus', methods=['POST'])
def filter_job_status():
    company_log_id = request.form.get('company_id')
    status_filter = request.form.get('status_filter')

    cursor = db_conn.cursor()

    # Modify the SQL query to filter by comp_id and job_status
    sql_query = "SELECT comp_id, job_id, job_name, job_description, job_status FROM internship WHERE comp_id = %s AND job_status = %s"
    cursor.execute(sql_query, (company_log_id, status_filter))

    filtered_job_data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyViewJobs.html', company_log_id=company_log_id, company_job_data=filtered_job_data)


# Change Job Status from ACTIVE to INACTIVE and vice versa
@app.route('/updateJobStatus', methods=['POST'])
def update_job_status():
    company_log_id = session.get('company_id')
    job_id = request.form.get('job_id')
    current_status = request.form.get('job_status')

    cursor = db_conn.cursor()

    # Determine the new status
    new_status = 'INACTIVE' if current_status == 'ACTIVE' else 'ACTIVE'

    # Update the job status in the database
    sql_query = "UPDATE internship SET job_status = %s WHERE comp_id = %s AND job_id = %s"
    cursor.execute(sql_query, (new_status, company_log_id, job_id))
    db_conn.commit()

    # Modify the SQL query to filter by comp_id
    sql_query = "SELECT comp_id, job_id, job_name, job_description, job_status FROM internship WHERE comp_id = %s"
    cursor.execute(sql_query, (company_log_id,))

    company_job_data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyViewJobs.html', company_log_id=company_log_id, company_job_data=company_job_data)

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
            # job_id = request.form.get('job_id')
            job_name = request.form.get('job_name')
            job_description = request.form.get('job_desc')
            job_files = request.files.get('job_files')

            job_id = str(company_log_id) + "_" + str(job_name)
            job_status = "ACTIVE"

            job_img_file_name = str(company_log_id) + "_" + str(job_id) + "_file.pdf"

            job[company_log_id] = { #rember to put = { }
                'job_id' : job_id,
                'job_name' : job_name,
                'job_description' : job_description,
                'job_file_name' : job_img_file_name,
                'job_status' : job_status
            }

            insert_sql_comp = "INSERT INTO internship VALUES (%s, %s, %s, %s, %s, %s)"
            cursor = db_conn.cursor()

            if job_files.filename == "":
                job_img_file_name = None
                try:
                    cursor.execute(insert_sql_comp, (company_log_id, job_id, job_name, job_description, job_img_file_name, job_status))
                    db_conn.commit()

                except Exception as e:
                    return str(e)

                finally:
                    cursor.close()

                return "Job posted successfully!"
            
            else:
                try:
                    cursor.execute(insert_sql_comp, (company_log_id, job_id, job_name, job_description, job_img_file_name, job_status))
                    db_conn.commit()
                    # Upload image file in S3 
                    job_img_in_s3 = job_img_file_name
                    s3 = boto3.resource('s3')

                    try:
                        print("Data inserted...Uploaded to S3")
                        s3.Bucket(custombucket).put_object(Key=job_img_in_s3, Body=job_files)
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

# Download Files in View Job 
@app.route('/downloadJobFile', methods=['GET'])
def download_job_file():
    job_file_name = request.args.get('job_file_name')

    # Ensure job_file_name is not empty
    if job_file_name is None:
        return "File name not provided."

    # Define the S3 bucket and key for the file
    s3_bucket = custombucket
    s3_key = job_file_name
    # Use Boto3 to download the file from S3
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')  # Use resource, not client

    try:

        # Download the file from S3 into memory
        s3_object = s3_resource.Object(s3_bucket, s3_key)
        file_data = s3_object.get()['Body'].read()

        # Create an in-memory stream to send the file as an attachment
        file_stream = BytesIO(file_data)

        # Return the file to the user for download with the specified filename
        return send_file(file_stream, as_attachment=True, download_name=job_file_name)


    except botocore.exceptions.NoCredentialsError:
        return "AWS credentials not found."
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return "File not found."
        else:
            return f"Error downloading file: {str(e)}", 500

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

# Redirect to Staff register page
@app.route("/toStaffRegister")
def toStaffRegister():
    return render_template('StaffRegister.html')

    
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

@app.route("/studentData", methods=['GET'])
def student_data():
    cursor = db_conn.cursor()
    cursor.execute("SELECT std_id, std_first_name, std_last_name, std_pass, assign_status FROM studentInformation")
    students = cursor.fetchall()
    cursor.close()

    return render_template('DisplayStudent.html', students=students)


# Display Supervisors
@app.route("/supervisorData", methods=['GET'])
def supervisor_data():
    cursor = db_conn.cursor()
    cursor.execute("SELECT spv_id, spv_name, spv_pass, spv_contact, spv_email, spv_subject FROM supervisorInformation")
    supervisors = cursor.fetchall()

    cursor.close()

    return render_template('DisplaySupervisors.html', supervisors=supervisors)

# Display Staffs
@app.route("/staffData", methods=['GET'])
def staff_data():
    cursor = db_conn.cursor()
    cursor.execute("SELECT stf_id, stf_name, staff_pass FROM staffInformation")
    staffs = cursor.fetchall()

    cursor.close()

    return render_template('DisplayStaffs.html', staffs=staffs)

# Update the route for company approval and rejection
@app.route("/approveCompany", methods=['POST'])
def approve_company():
    company_id = request.form.get('company_id')
    action = request.form.get('action')

    if action == 'approve':
        update_status = 'Approved'
    elif action == 'reject':
        update_status = 'Rejected'
    else:
        return "Invalid action."

    # Update the company status in the database
    update_sql = "UPDATE company SET comp_status = %s WHERE comp_id = %s"
    cursor = db_conn.cursor()
    
    try:
        cursor.execute(update_sql, (update_status, company_id))
        db_conn.commit()
    except Exception as e:
        db_conn.rollback()
        return str(e)
    finally:
        cursor.close()

    return redirect('/validateCompany')

# Update the route for displaying pending companies
@app.route("/validateCompany", methods=['GET'])
def validate_company():
    cursor = db_conn.cursor()
    cursor.execute("SELECT comp_id, comp_name, comp_industry, comp_address, comp_password, comp_status FROM company WHERE comp_status = 'Pending'")
    pending_companies = cursor.fetchall()
    cursor.close()

    return render_template('ValidateCompany.html', pending_companies=pending_companies)

# Route for displaying student assignments with details
@app.route("/assignmentDisplay", methods=['GET'])
def display_student_assignment():
    cursor = db_conn.cursor()

    # Fetch data from supervisorHandle and join with studentInformation and supervisorInformation
    cursor.execute("""
        SELECT 
            supervisorHandle.std_id, 
            studentInformation.std_first_name, 
            studentInformation.std_last_name, 
            supervisorInformation.spv_name
        FROM supervisorHandle
        LEFT JOIN studentInformation ON supervisorHandle.std_id = studentInformation.std_id
        LEFT JOIN supervisorInformation ON supervisorHandle.spv_id = supervisorInformation.spv_id
    """)
    assignments = cursor.fetchall()
    print(assignments)  # Add this line for debugging
    cursor.close()

    return render_template('DisplayStudentAssignment.html', assignments=assignments)

@app.route("/assignStudents", methods=['GET', 'POST'])
def assign_students():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        supervisor_id = request.form.get('supervisor_id')

        # Check if the student's assign_status is "Pending" before assigning
        cursor = db_conn.cursor()
        select_sql = "SELECT assign_status FROM studentInformation WHERE std_id = %s"
        cursor.execute(select_sql, (student_id,))
        status = cursor.fetchone()

        if status and status[0] == 'Pending':
            # Perform the assignment by inserting a new record in the supervisorHandle table
            insert_sql = "INSERT INTO supervisorHandle (spv_id, std_id) VALUES (%s, %s)"
            
            try:
                cursor.execute(insert_sql, (supervisor_id, student_id))
                # Update the student's assign_status to "Assigned"
                update_sql = "UPDATE studentInformation SET assign_status = 'Assigned' WHERE std_id = %s"
                cursor.execute(update_sql, (student_id,))
                db_conn.commit()
            except Exception as e:
                db_conn.rollback()
                return str(e)
            finally:
                cursor.close()

            # Redirect to a confirmation page or another relevant page
            return redirect('/assignmentDisplay')
        else:
            return "Student cannot be assigned. Please check the student's status."
    
    return render_template('AssignStudents.html')

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

# Redirect to SupervisorHomePage
@app.route("/toSupervisorHomePage")
def toSupervisorHomePage():
    return render_template('SupervisorHomePage.html')


# Redirect to PortFolioEricTan
@app.route("/toPortfolioEricTan")
def toPortfolioEricTan():
    return render_template('PortfolioEricTan.html')

# Redirect to viewSupervisorList
@app.route("/toDisplaySupervisors", methods=['GET'])
def display_supervisors():
    cursor = db_conn.cursor()
    cursor.execute("SELECT spv_id, spv_name, spv_pass, spv_contact, spv_email FROM supervisorInformation")
    supervisors = cursor.fetchall()

    cursor.close()
    print("Supervisors:", supervisors)
    return render_template('DisplaySupervisors.html', supervisors=supervisors)

# Redirect to viewStudentList
@app.route("/toDisplayStudent", methods=['GET'])
def display_student():
    cursor = db_conn.cursor()
    cursor.execute("SELECT std_id, std_first_name, std_last_name, std_pass FROM studentInformation")
    students = cursor.fetchall()

    cursor.close()
    print("Students:", students)
    return render_template('DisplayStudent.html', students=students)

# Redirect to viewStaffList
@app.route("/toDisplayStaffs", methods=['GET'])
def display_staffs():
    cursor = db_conn.cursor()
    cursor.execute("SELECT stf_id, stf_name, staff_pass FROM staffInformation")
    staffs = cursor.fetchall()

    cursor.close()
    print("Staffs:", staffs)
    return render_template('DisplayStaffs.html', staffs=staffs)



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


# Display Intern Application
@app.route("/internData", methods=['GET'])
def intern_data():
    cursor = db_conn.cursor()
    cursor.execute("SELECT std_id, cmp_id, cmp_name FROM student")
    interns = cursor.fetchall()

    cursor.close()
    print("Interns:", interns)
    return render_template('InternApplication.html', interns=interns)

# Accept Intern
@app.route("/acceptIntern/<string:id>", methods=['GET'])
def accept_intern(id): 
    print(id)
    return render_template('SupervisorHomePage.html')

# Reject Intern
@app.route("/rejectIntern/<string:id>", methods=['GET'])
def reject_intern(id): 
    print(id)
    return render_template('SupervisorHomePage.html')



 
    
   


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