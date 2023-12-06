import uuid
from mysql_connector import MySQLConnector
import json


def connect_to_database():
    pass

def post_new_user(param_dict):

    if param_dict['user_type'].lower() == "student":
        # write to the student table
        response_dict = post_new_student(param_dict)
    elif param_dict['user_type'].lower() == "instructor":
        # write to the instructor table
        response_dict = post_new_instructor(param_dict)

    return response_dict

def post_new_student(param_dict):
    user_uuid = str(uuid.uuid4())
    first_name = param_dict['first_name']
    last_name = param_dict['last_name']
    dept_name = param_dict['dept_name']
    email = param_dict['email']

    bool_success = False

    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Update a data row in the table
    try:
        cursor.execute(f"INSERT INTO Student(studentID, studentFirstName, studentLastName, deptName, email) \
                       VALUES('{user_uuid}','{first_name}','{last_name}','{dept_name}', '{email}')")
    except:
        print("Some error occured while inserting student")
        user_uuid = None
    else:
        bool_success = True
    
    print("Inserted",cursor.rowcount,"row(s) of data.")
    sql_connector.close_connection()

    response = {
        "user_id": user_uuid,
        "success": bool_success
    }


    return response
    

def post_new_instructor(param_dict):
    user_uuid = str(uuid.uuid4())
    first_name = param_dict['first_name']
    last_name = param_dict['last_name']
    dept_name = param_dict['dept_name']
    email = param_dict['email']

    bool_success = False

    # Get the SQL connector and connect to DB
    sql_connector = MySQLConnector()
    sql_connector.connect_to_db()

    cursor = sql_connector.get_cursor()
    # Update a data row in the table
    try:
        cursor.execute(f"INSERT INTO Instructor(instructID, instructFirstName, instructLastName, deptName, email) \
                        VALUES('{user_uuid}','{first_name}','{last_name}','{dept_name}', '{email}')")
    except:
        print("Some error occured when inserting instructor")
        user_uuid = None
    else:
        bool_success = True

    print("Inserted",cursor.rowcount,"row(s) of data.")
    sql_connector.close_connection()
   

    response = {
        "user_id": user_uuid,
        "success": bool_success
    }

    return response



if __name__ == "__main__":
    
    input_params1 = {
        "user_type": "instructor",
        "first_name": "Bill",
        "last_name": "Doe",
        "dept_name": "Health",
        "email": "bd@example.com"
    }

    input_params2 = {
        "user_type": "student",
        "first_name": "Bill",
        "last_name": "Doe",
        "dept_name": "Health",
        "email": "bdo@example.com"

    }

    response_dict1 = post_new_user(input_params1)

    response_dict2 = post_new_user(input_params2)

    print(json.dumps(response_dict1))

    print(json.dumps(response_dict2))






