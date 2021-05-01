# this is to import Flask, render_template(to run the template/.html files)
from flask import Flask, render_template, request,redirect, url_for, flash
from flask.helpers import flash, url_for
from pymysql import connections, cursors 
import os 
import boto3 

from rds_db import * 

# this is for Flask instant
app = Flask(__name__)

app.secret_key = 'dont tell anyone'
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
@app.route('/')
def index():
    # calling index.html file here.
    return render_template('index.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/employee')
def employee():
    return render_template('employee.html')

@app.route('/createCustplan')
def createCustplan():
    return render_template('createCustplan.html')

@app.route('/searchempid',methods=['POST'])
def searchempid():
    if request.method == "POST":
        Employee_ID = request.form['Employee_ID']
        cursor = db_conn.cursor()
        # search by author or book
        cursor.execute("SELECT *from Employee WHERE Employee_ID =%s",(Employee_ID))
        db_conn.commit()
        data = cursor.fetchall()
        cursor.close()
        return render_template('createCustplan.html', data=data)
    return render_template('createCustplan.html')

@app.route("/addcustomizationdetail", methods=['POST','GET'])
def addcustomizationdetail():
       
        Employee_ID=request.form['Employee_ID']
        Customer_ID = request.form['Customer_ID']
        Name = request.form['Name']
        Phone = request.form['Phone']
        Email = request.form['Email']
        Address = request.form['Address']
        City = request.form['City']
        State = request.form['State']
        Zip = request.form['Zip']
        #####################################
        Vin = request.form['Vin']
        Make =request.form['Make']
        Model=request.form['Model']
        Year=request.form['Year']
        Engine=request.form['Engine']
        Trim = request.form['Trim']
        Interior=request.form['Interior']
        Exterior=request.form['Exterior']
        Body_Condition=request.form['Body_Condition']
        Frame_Condition=request.form['Frame_Condition']
        Interior_Condition=request.form['Interior_Condition']
        Engine_Condition=request.form['Engine_Condition']
        ################################################
        Plan_ID = request.form['Plan_ID']
        Estimated_delivery_date=request.form['Estimated_delivery_date']
        Item_ID = request.form['Item_ID']
        Item_name=request.form['Item_name']
        Item_Description=request.form['Item_Description']
        Item_completion_estimation=request.form['Item_completion_estimation']
        ##################################################
        #######  GET PART DETAIL######################
        part_name=request.form['part_name']
        part_quantity=request.form['part_quantity']
        labor_name=request.form['labor_name']
        cursor = db_conn.cursor()
        #search for part ID from the part table
        cursor.execute("SELECT part_ID,part_price from Part WHERE part_name =%s",(part_name))
        db_conn.commit()
        data1 = cursor.fetchall()
        
        for x in data1:
            d = x[0]
            d =str(d)
            g= int(part_quantity)*int(x[1])
            g =str(g)
        
        #search for Labor ID from the labor table
        cursor.execute("SELECT labor_ID,labor_cost from Labor WHERE labor_name =%s",(labor_name))
        db_conn.commit()
        data2 = cursor.fetchall()
        
        for x in data2:
            lid = x[0]
            lid =str(lid)
            lct= str(x[1])

         #calculating item_estimation_price and total_estimation price
        itemtct= int(g) + int(lct)
        itemtct=str(itemtct)
        totestipr = itemtct

        # insert vlaues into customer table
        cursor=db_conn.cursor()
        insert_sql = "INSERT INTO customer VALUES (%s, %s, %s, %s, %s , %s , %s , %s)"
        
        cursor.execute(insert_sql, (Customer_ID, Name, Phone, Email, Address , City , State , Zip))
        db_conn.commit()
        
         # insert vlaues into vehicle table
        q1= "INSERT INTO Vehicle(VIN, Make, Model, Year, Engine, Trim, Interior, Exterior, Body_Condition, Frame_Condition, Interior_Condition, Engine_Condition, Cust_ID) VALUES (%s ,%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val=(Vin, Make, Model, Year, Engine, Trim, Interior, Exterior, Body_Condition, Frame_Condition, Interior_Condition, Engine_Condition, Customer_ID)
        cursor.execute(q1,val)
        db_conn.commit()

         # insert vlaues into customization plan table
        insert_plan = "INSERT INTO Customization_plan(Plan_ID, Estimated_delivery_date, Total_estimated_Price) VALUES (%s, %s, %s)"
        v2= (Plan_ID, Estimated_delivery_date, totestipr)
        cursor.execute(insert_plan,v2)
        db_conn.commit()

         # insert vlaues into customization detail table
        insert_plan = "INSERT INTO Customization_detail(Plan_ID, Customer_ID, VIN, Employee_ID) VALUES (%s, %s, %s, %s)"
        v2= (Plan_ID, Customer_ID, Vin, Employee_ID)
        cursor.execute(insert_plan,v2)
        db_conn.commit()

        #insert into Item table
        query0 ="INSERT INTO Item(Item_ID, Item_name, Item_Description,Item_completion_estimation,PN_ID, item_estimated_price, Emp_ID) VALUES (%s ,%s , %s ,%s ,%s, %s, %s)"
        valus = (Item_ID, Item_name, Item_Description, Item_completion_estimation, Plan_ID, itemtct, Employee_ID)
        cursor.execute(query0,valus)
        db_conn.commit()
        
        #insert values into part detail table
        query ="INSERT INTO Part_Detail(Part_ID, Itm_ID, part_quantity, part_total_cost) VALUES (%s ,%s , %s ,%s)"
        values = (d,Item_ID, part_quantity, g)
        cursor.execute(query,values)
        db_conn.commit()

        #insert values into labor detail table
        query1 ="INSERT INTO Labor_detail(Labor_ID, Item_ID, labor_total_cost) VALUES (%s , %s ,%s)"
        vals = (lid,Item_ID, lct)
        cursor.execute(query1,vals)
        db_conn.commit()
        cursor.close()
        flash('Customization form is ready.')
        return render_template('createCustplan.html',data1=data1)




@app.route('/emplworkdet')
def emplworkdet():
    return render_template('emplworkdet.html')

@app.route("/manageplan")
def manageplan():
    return render_template('emplworkdet.html')

#this route is for searching the specific employee
@app.route("/searchplan", methods=['POST'])
def searchplan():
    if request.method == "POST":
        #Employee_ID = request.form['Employee_ID']
        Plan_ID = request.form['Plan_ID']
        cursor = db_conn.cursor()
        # search by author or book
        cursor.execute("SELECT *from Customization_detail WHERE Plan_ID =%s",(Plan_ID))
        db_conn.commit()
        data = cursor.fetchall()
        return render_template('emplworkdet.html', data=data)
    return render_template('emplworkdet.html')

#this route is for show all the employee 
@app.route("/showallplan", methods=['POST'])
def showallplan():
    Employee_ID =request.form['Employee_ID']
    cur = db_conn.cursor()
    cur.execute("SELECT *from Customization_detail WHERE Employee_ID=%s",(Employee_ID)) 
    data = cur.fetchall()
    cur.close()
    return render_template('emplworkdet.html', plan=data)

#this route is for update the costomization plan
@app.route('/editplan/<planid>', methods=['POST', 'GET'])
def editplan(planid):
   
    
    cur = db_conn.cursor()
    cur.execute("SELECT *from Customization_detail WHERE Plan_ID=%s",(planid)) 
    cust_detail = cur.fetchall()
    for x in cust_detail:
        cust_id=x[1]
    cur.execute("SELECT *from customer WHERE Customer_ID=%s",(cust_id)) 
    cust_info = cur.fetchall()
    cur.execute("SELECT *from Customization_plan WHERE Plan_ID=%s",(planid)) 
    cust_plan = cur.fetchall()
    #return redirect(url_for('updatecustplan'),cust_detail=cust_detail,cust_plan=cust_plan, cust_info=cust_info)
    return render_template('updatecustplan.html', plid=cust_detail[0], cust_detail=cust_detail,cust_plan=cust_plan, cust_info=cust_info)

@app.route('/updatecustplan')
def updatecustplan():
    return render_template('updatecustplan.html')

#this route is for update the employee
@app.route('/updatecustmization/<pid>', methods=['POST'])
def updatecustmization(pid):
   
    if request.method == 'POST':
       # id = request.form['id']
        Totalprice = request.form['Totalprice']
        deposit_amount = request.form['deposit_amount']
        StartDate = request.form['StartDate']
        Esti_deliver = request.form['Esti_deliver']
        subtotal_price= request.form['subtotal_price']
        tax = request.form['tax']
        amount_due = request.form['deposit_amount']
        payment_method = request.form['payment_method']
        pay_date = request.form['pay_date']

        cursor = db_conn.cursor()
       
        cursor.execute("""
        UPDATE Customization_plan
        SET Total_Estimated_Price=%s, deposite_amount=%s, StartDate=%s, Estimated_delivery_date=%s, Subtotal_price=%s,  tax_amount=%s, amount_due=%s, payment_method=%s, payment_date=%s
        WHERE Plan_ID=%s
        """, (Totalprice, deposit_amount, StartDate, Esti_deliver, subtotal_price, tax, amount_due, payment_method, pay_date, pid))
        
        #flash('Customization Plan Updated Successfully')
        db_conn.commit()
        return render_template('emplworkdet.html')


@app.route('/modperdet')
def modperdet():
    return render_template('modperdet.html')

#this route is for edit employee detail 
@app.route('/edit', methods=['POST'])
def edit():
    Employee_ID=request.form['Employee_ID']
    print("%%%%%%%%%%%%")
    #print(Employee_ID)
    cur = db_conn.cursor()
    cur.execute('SELECT * FROM Employee WHERE Employee_ID = %s', (Employee_ID))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('modperdet.html', emp = data)

#this route is for update the employee
@app.route('/updateemp/<id>', methods=['POST'])
def update(id):
   
    if request.method == 'POST':
       # id = request.form['id']
        name = request.form['name']
        title = request.form['title']
        phone = request.form['phone']
        email = request.form['email']
        cur = db_conn.cursor()
        cur.execute("""
        UPDATE Employee 
        SET Name = %s, 
            Title = %s, 
            Phone_number = %s, 
            Email = %s
        WHERE Employee_ID = %s""",
        (name, title, phone, email, id))
        flash('Employee Updated Successfully')
        db_conn.commit()
        return redirect(url_for('modperdet'))

@app.route('/management')
def management():
    return render_template('management.html')

# this is important to run the code by python version directly without going to virtual environment and run the code wtih flask run 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)