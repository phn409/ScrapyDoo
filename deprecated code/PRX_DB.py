from APS import APS
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import mysql.connector

## Cell one, Make table

PRX=APS(abbrev='prx')
PRX.indexVolumes()
#Get total number of issues
PRX.indexIssues(verbose=True, skip=3) #Unused test parameters: 

print('link current issue:',PRX.link())
print('link volume 3 issue 2:',PRX.link(vol=2,iss=4))
print('total number of volumes:',PRX.nVolumes)
print('total number of issues:',PRX.nIssues)

#Scraping to PD Dataframe
#-----------------STATUS: Part way------------------------------------------#
#Create data frame containing the links to all articles
#vi = np.array(range(PRX.nVolumes)) + 1 #volume index
#ni = np.array(range(PRX.nIssues)) + 1 #issue index
vol_iss = {'Vol': list(reversed([*PRX.volumes,])), 'Iss':[]}
for v in vol_iss['Vol']:
    #Print number of issues in each volume
    PRX.indexIssues(All = False, num = int(v))
    ni = PRX.volumes[v].nIssues
    vol_iss['Iss'].append(ni)
    print('Volume: {}, Issues: {}'.format(v, ni))

#to DF
VIDF = pd.DataFrame(vol_iss)
print(VIDF)


#%%
#PD Dataframe to SQL
## Cell two
#-----------------STATUS: Incomplete------------------------------------------#

# ====== Connection ====== #
# Connecting to mysql by providing a sqlachemy engine
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
#engine = create_engine(sqlroot, echo=False)
VIDF.to_sql(name='prx',con=engine,if_exists='replace', index=False) #if_exists='append'




#%%
#Cell 3 Extract information from DB
"""
mydb = mysql.connector.connect(
  host="localhost", #PHNSQL
  user="root",
  passwd="MySQLPassword",
  database = "MySQL"
)

# ====== Reading table ====== #
# Reading Mysql table into a pandas DataFrame
#sql_cmd = 'SELECT * FROM prx'
#sql_cmd = "SELECT * FROM prx WHERE Iss < 4"
sql_cmd = "SELECT * FROM prx WHERE Iss > 3"
#DB_fetch = pd.read_sql('SELECT * FROM customers', engine)
DB_fetch = pd.read_sql(sql_cmd, engine)
print(DB_fetch)
#----------------------------------------------------------------------------#
#Output DB fetch as line-by-line output
#mycursor.execute(sql_cmd)
#
#myresult = mycursor.fetchall()
#
#for x in myresult:
#    print(x)
#%%

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
