from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import mysql.connector

database_username = 'root'
database_password = 'MySQLPassword'
database_ip       = '127.0.0.1'
database_name     = 'MySQL'
#sqlroot = 'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
#                       format(database_username, database_password, 
#                              database_ip, database_name)
engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                       format(database_username, database_password, 
                              database_ip, database_name)) #,echo=False


#%%
#Cell 3 Extract information from DB
mydb = mysql.connector.connect(
  host="localhost", #PHNSQL
  user="root",
  passwd="MySQLPassword",
  database = "MySQL"
)

# ====== Reading table ====== #
# Reading Mysql table into a pandas DataFrame
sql_cmd = 'SELECT * FROM prx'
#sql_cmd = "SELECT * FROM prx WHERE Iss < 4"
#sql_cmd = "SELECT * FROM prx WHERE Iss > 3"
#DB_fetch = pd.read_sql('SELECT * FROM customers', engine)
#DB_fetch = pd.read_sql(sql_cmd, engine)
#print(DB_fetch)
#----------------------------------------------------------------------------#
#Output DB fetch as line-by-line output
mycursor=mydb.cursor()
mycursor.execute(sql_cmd)
#
myresult = mycursor.fetchall()
#
for x in myresult:
    print(x)
#%%

"""
#Cell 4 Use SQL commands to modify table
#Delete table row
mycursor = mydb.cursor()
sql = "DROP TABLE IF EXISTS prx"

mycursor.execute(sql)
#---------------------------------------------------------------------------------#
#Update a table row
#sql = "UPDATE customers SET address = %s WHERE address = %s"
#val = ("Valley 345", "Canyon 123")
#mycursor.execute(sql, val)
#mydb.commit()
#print(mycursor.rowcount, "record(s) affected")
"""
