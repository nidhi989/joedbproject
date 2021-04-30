# this is the new app.py with inserting and show all employee function. 

# this is to import Flask, render_template(to run the template/.html files)
from flask import Flask, render_template, request, flash, url_for, redirect
from pymysql import connections 
import os 
import boto3 
from rds_db import * #import rds_db as db
# this is for Flask instant
app = Flask(__name__)
app.secret_key = "my secret key"

#to set the rds_db as the database for the website
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
table = 'joechopdatabase';

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

@app.route("/manageemp")
def manageemp():
    return render_template('manageemp.html')

#this route is for searching the specific employee
@app.route("/modifyemp", methods=['POST'])
def modifyemp():
    if request.method == "POST":
        Employee_ID = request.form['Employee_ID']
        cursor = db_conn.cursor()
        # search by author or book
        cursor.execute("SELECT *from Employee WHERE Employee_ID =%s",(Employee_ID))
        db_conn.commit()
        data = cursor.fetchall()
        return render_template('manageemp.html', data=data)
    return render_template('manageemp.html')


#this route is for show all the employee 
@app.route("/showall", methods=['POST'])
def showall():
    cur = db_conn.cursor()
    cur.execute("SELECT *FROM Employee") 
    data = cur.fetchall()
    cur.close()
    return render_template('manageemp.html', emp=data)

@app.route("/insertemp", methods=['POST'])
def insertemp():
    if request.method == 'POST':
        cur = db_conn.cursor()
        id = request.form['id']
        name = request.form['name']
        title = request.form['title']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute("INSERT INTO Employee (Employee_ID, Name, Title, Phone_number, Email) VALUES (%s, %s, %s, %s, %s)",(id, name, title, phone, email))
        db_conn.commit()
        flash('Employee Added Successfully')
        #data=cur.fetchall()
        #cur.close()
        return redirect(url_for('manageemp'))

@app.route("/edit/<id>", methods=['Post', 'GET'])
def edit(id):
    cur = db_conn.cursor()
    cur.execute('SELECT * FROM Employee WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', empployee = data[0])


@app.route("/review")
def review():
    return render_template('review.html')

# this is important to run the code by python version directly without going to virtual environment and run the code wtih flask run 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


