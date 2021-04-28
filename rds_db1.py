customhost = "joechopdatabase.cshuzwurdyzv.us-east-2.rds.amazonaws.com"
customuser = "admin"
custompass = "admin531"
customdb = "joechopdatabase"
custombucket = "sqljoe"
customregion = "us-east-2a"


# import pymysql
# import aws_credentials as rds
# conn = pymysql.connect(
#         host = "joechopdatabase.cshuzwurdyzv.us-east-2.rds.amazonaws.com",
#         user = "admin",
#         password = "admin531",
#         db = "joechopdatabase",
#         s3bucket = "sqljoe",
#         awsregion = "us-east-2a"

#         )

#Table Creation
#cursor=conn.cursor()
#create_table="""
#create table Details (name varchar(200),email varchar(200),comment varchar(200),gender varchar(20) )
#
#"""
#cursor.execute(create_table)


# def insert_details(name,email,comment,gender):
#     cur=conn.cursor()
#     cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name,email,comment,gender))
#     conn.commit()

# def get_details():
#     cur=conn.cursor()
#     cur.execute("SELECT *  FROM Details")
#     details = cur.fetchall()
#     return details
