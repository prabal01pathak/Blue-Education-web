import sqlite3
from string import Template
conn = sqlite3.connect("test.db")
#conn.execute("Create Table user (username var, password var)")
#conn.execute("INSERT INTO user values ('prabal','pathak')")
#conn.commit()
#data = Template("INSERT INTO user values ('$username','$password')")
username ='prabl or 1=1'
password='pathak'
cursor = conn.execute("select * from user where username = '%s'" % "';--")
data = cursor.fetchall()
print(data)
