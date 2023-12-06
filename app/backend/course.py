from mysql_connector import MySQLConnector
import json

def add_course(param_dict):
    if param_dict['user_type'].lower() == "student":
        # write to the student table
        response = student_add_course(param_dict)
    elif param_dict['user_type'].lower() == "instructor":
        # write to the instructor table
        response = instructor_add_course(param_dict)

    return response

def student_search_course(param_dict):
    user_uuid = param_dict['user_id']
    bool_success = False

    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Update a data row in the table
    course_code = param_dict['course_code']

    # Read data
    try:
        cursor.execute(f"SELECT courseCode, courseName, secNum, secSemester, secYear from Course natural join Section where courseCode='{course_code}'")
        rows = cursor.fetchall()
    except:
        print("Something went wrong when getting student courses")
    else:
        bool_success = True
    
    sql_connector.close_connection()

    print("Read",cursor.rowcount,"row(s) of data.")

    response = {
        "courses": rows,
        "success": bool_success
    }

    return response


def student_add_course(param_dict):
    # insert into the enrolled table
    # input: user_uuid, course_code, sec_number, sec_semester, sec_year
    user_uuid = param_dict['user_id']
    bool_success = False

    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Update a data row in the table

    course_code = param_dict['course_code']
    sec_number = param_dict['sec_number']
    sec_semester = param_dict['sec_semester']
    sec_year = param_dict['sec_year']

    try:
        cursor.execute(f"INSERT INTO Enrolled(studentID, courseCode, secNum, secSemester, secYear) \
                        VALUES('{user_uuid}', '{course_code}', '{sec_number}', '{sec_semester}', '{sec_year}')")
    except:
        print("Some error occured when inserting Enrolled")
    else:
        bool_success = True

    print("Inserted",cursor.rowcount,"row(s) of data.")

    sql_connector.close_connection()
   
    response = {
        "user_id": user_uuid,
        "success": bool_success
    }

    return response

def instructor_add_course(param_dict):
    # add the course into the course table and section table
    # add the instructor into the teaches table

    # input: user_uuid, course_code, course_name, sec_number, sec_semester, sec_year
    user_uuid = param_dict['user_id']
    bool_success = False

    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Update a data row in the table

    course_code = param_dict['course_code']
    course_name = param_dict['course_name']

    print(course_code)
    print(course_name)

    try:
        cursor.execute(f"INSERT INTO Course(courseCode, courseName) \
                        VALUES('{course_code}','{course_name}')")
    except Exception as ex:
        print("Some error occured when inserting Course")
        print(ex)

    sec_number = param_dict['sec_number']
    sec_semester = param_dict['sec_semester']
    sec_year = param_dict['sec_year']

    try:
        cursor.execute(f"INSERT INTO Section(courseCode, secNum, secSemester, secYear) \
                        VALUES('{course_code}', '{sec_number}', '{sec_semester}', '{sec_year}')")
    except:
        print("Some error occured when inserting Section")
    
    try:
        cursor.execute(f"INSERT INTO Teaches(instructID, courseCode, secNum, secSemester, secYear) \
                        VALUES('{user_uuid}', '{course_code}', '{sec_number}', '{sec_semester}', '{sec_year}')")
    except:
        print("Some error occured when inserting Teaches")
    else:
        bool_success = True

    print("Inserted",cursor.rowcount,"row(s) of data.")

    sql_connector.close_connection()
   
    response = {
        "user_id": user_uuid,
        "success": bool_success
    }

    return response

# def instructor_add_students(param_dict):

#     bool_success = False

#     # Get the SQL connector and connect to DB
#     sql_connector = MySQLConnector()
#     sql_connector.connect_to_db()

#     cursor = sql_connector.get_cursor()
#     # Update a data row in the table
#     try:
#         cursor.execute(f"INSERT INTO Instructor(instructID, instructFirstName, instructLastName, deptName, email) \
#                         VALUES('{user_uuid}','{first_name}','{last_name}','{dept_name}', '{email}')")
#     except:
#         print("Some error occured when inserting instructor")
#         user_uuid = None
#     else:
#         bool_success = True

#     print("Inserted",cursor.rowcount,"row(s) of data.")
#     sql_connector.close_connection()
   

#     response = {
#         "user_id": user_uuid,
#         "success": bool_success
#     }

#     return response



def display_courses(param_dict):

    if param_dict['user_type'].lower() == "student":
        # write to the student table
        response_dict = student_display_courses(param_dict)
    elif param_dict['user_type'].lower() == "instructor":
        # write to the instructor table
        response_dict = instructor_display_courses(param_dict)

    return response_dict

def student_display_courses(param_dict):
    user_uuid = param_dict['user_id']
    # Select from Enrolled Table to find which courses studens are enrolled in
    # return this as a list of courses
    
    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Read data
    try:
        cursor.execute(f"SELECT courseCode, courseName, secNum, secSemester, secYear from Enrolled natural join Course where studentID='{user_uuid}'")
        rows = cursor.fetchall()
    except:
        print("Something went wrong when getting student courses")
    
    sql_connector.close_connection()

    print("Read",cursor.rowcount,"row(s) of data.")

    response = {
        "user_id":  user_uuid,
        "courses":  rows
    }

    return response


def instructor_display_courses(param_dict):
    # Select from Teaches Table to find which courses this instructor currently teaches
    # return this as a list of courses
    user_uuid = param_dict['user_id']
    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Read data
    try:
        cursor.execute(f"SELECT courseCode, courseName, secNum, secSemester, secYear from Teaches natural join Course where instructID='{user_uuid}'")
        rows = cursor.fetchall()
    except:
        print("Something went wrong when getting instructor courses")

    sql_connector.close_connection()
    print("Read",cursor.rowcount,"row(s) of data.")

    response = {
        "user_id":  user_uuid,
        "courses":  rows
    }

    return response
    

def delete_course(param_dict):
    pass

def modify_course(param_dict):
    pass

if __name__ == "__main__":
    input_params = {
        "user_id": "bbed4a53-d988-472d-a5db-9a3c4519774e",
        "user_type": "instructor"
    }
    print(json.dumps(display_courses(input_params)))

    # course_code, course_name, sec_number, sec_semester, sec_year
    input_params1 = {
        "user_id": "bbed4a53-d988-472d-a5db-9a3c4519774e",
        "user_type": "instructor",
        "course_code": "ECE457A",
        "course_name": "Cooperative and Adaptive Algos",
        "sec_number": 1,
        "sec_semester": "Spring",
        "sec_year": 2023
    }

    print(json.dumps(add_course(input_params1)))

    input_params2 = {
        "user_id": "9d7b62eb-4b6e-41d9-838e-711bfd6e08a7",
        "user_type": "student",
        "course_code": "ECE457A",
        "sec_number": 1,
        "sec_semester": "Spring",
        "sec_year": 2023
    }
    print(json.dumps(add_course(input_params2)))

    input_params3 = {
        "user_id": "9d7b62eb-4b6e-41d9-838e-711bfd6e08a7",
        "user_type": "student",
        "course_code": "ECE457A"
    }

    print(json.dumps(student_search_course(input_params3)))
