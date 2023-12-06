import json
from ..backend.signup import post_new_user
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

def test_register_instructor():
    input_params = {
        "user_type": "instructor",
        "first_name": "Bill",
        "last_name": "Doe",
        "dept_name": "Health",
        "email": "bd@example.com"
    }
    response_dict = post_new_user(input_params)

    print(json.dumps(response_dict))

def test_register_student():
    input_params = {
        "user_type": "student",
        "first_name": "Bill",
        "last_name": "Doe",
        "dept_name": "Health",
        "email": "bd@example.com"
    }
    response_dict = post_new_user(input_params)

    print(json.dumps(response_dict))

if __name__ == "__main__":
    test_register_instructor()
    test_register_student()


    
