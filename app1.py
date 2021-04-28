# this is to import Flask, render_template(to run the template/.html files)
from flask import Flask, render_template, request
from pymysql import connections 
import os 
import boto3 
from rds_db import * 
# this is for Flask instant
app = Flask(__name__)

#to set the rds_db as the database for the website
#import rds_db as db
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


# everytime you have to give route to run web application page.
@app.route("/")
def index():
    # calling index.html file here.
    return render_template('index.html')

@app.route("/customer")
def customer():
    return render_template('customer.html')

@app.route("/employee")
def employee():
    return render_template('employee.html')

@app.route("/management")
def management():
    return render_template('management.html')

# this is important to run the code by python version directly without going to virtual environment and run the code wtih flask run 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
