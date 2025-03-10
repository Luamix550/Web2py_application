"""
This module contains the controller for student operations. 
It includes functions for viewing and registering students.
"""

import os
from http import HTTPStatus
from gluon import HTTP
from applications.SIP_application.modules.services.business_logic import student_service

def students_view():
    """Returns the path to the students view."""
    return response.stream(os.path.join(request.folder, 'static', 'build', 'index.html'))

def register():
    """Registers a new student."""
    try:
        if request.env.request_method != 'POST':
            raise HTTP(HTTPStatus.METHOD_NOT_ALLOWED)

        # Print request details for debugging
        print('request.env:', request.env)

        # Extract student data from the request vars
        student_data = request.vars

        # Check if student_data is None
        if student_data is None:
            raise HTTP(HTTPStatus.BAD_REQUEST, 'Student data not provided')

        # Validate student data
        if 'name' not in student_data or not student_data['name']:
            raise HTTP(HTTPStatus.BAD_REQUEST, 'Name is required')
        if 'email' not in student_data or not student_data['email']:
            raise HTTP(HTTPStatus.BAD_REQUEST, 'Email is required')

        # Create student and save in the database
        student_service.create_student(student_data, db)

        return dict(success=True)
    except Exception as e:
        raise HTTP(400, "controller error " + str(e)) from e
