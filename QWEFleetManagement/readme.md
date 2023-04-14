Flask Web Application Fleet Management

This is a Flask web application template that can be used as a starting point for building web applications.
Requirements

    Python 3.6+
    See requirements.txt for additional Python package dependencies.

Installation

Create and activate a virtual environment:

    python3 -m venv env
        
    source env/bin/activate

Install the required Python packages:
            
    pip install -r requirements.txt

Configuration

Copy the example.env file and rename it to .env. Change the values in the .env file to suit your needs.
Running the Application

To run the application, execute the following command:


python run.py

    Navigate to http://localhost:5000 in your browser.


Usage
Sign Up

To sign up for an account, navigate to the signup page (/signup) and enter a unique username and password.
Log In

To log in to your account, navigate to the login page (/login) and enter your username and password.
Protected Page

After logging in, you will be able to access the protected page (/protected) which requires authentication.
Logging Out

To log out of your account, navigate to the logout page (/logout).
License

This project is licensed under the MIT License. See the LICENSE file for more information.
