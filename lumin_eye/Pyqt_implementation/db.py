#-----------------------------------------------
#Connecting to server and creating new database
#-----------------------------------------------

import mysql.connector

def exec(dbuser, dbpass):
    #Connecting to server
    mydb = mysql.connector.connect(
                host = "localhost",
                user = dbuser,            
                password = dbpass,
                database="envision"
            )

    cursor = mydb.cursor()
    '''MariaDB [envision]> CREATE TABLE envision.login_info SELECT * FROM library.login_info;
        Query OK, 5 rows affected (0.064 sec)
        Records: 5  Duplicates: 0  Warnings: 0
        '''
    
    #Creating database
    cursor.execute("CREATE DATABASE IF NOT EXISTS envision")
    cursor.execute("USE envision")

    #Creating login table
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_info
    (name VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL PRIMARY KEY,
    password VARCHAR(30) NOT NULL)""")
    mydb.commit()




