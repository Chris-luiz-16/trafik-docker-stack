from flask import Flask, render_template
import mysql.connector
import os


app = Flask(__name__)

  
@app.route('/')  
def message(): 
  
  try:
        
    dataBase = mysql.connector.connect(
        host = database_host,
        user = database_user,
        passwd = database_password,
        database  = "college"
    )
    
    cursorObject = dataBase.cursor(dictionary=True)
    query = "select * from employees"
    cursorObject.execute(query)
    students = cursorObject.fetchall() 
    dataBase.close()
    
    return render_template('index.html.tmpl',students=students,hostname=hostname)

  except:
    
    return "<h3>Database Connection Error</h3>"
     


if __name__ == '__main__': 
  
  hostname = os.getenv('HOSTNAME',None)
  database_host = os.getenv('DATABASE_HOST',None)
  database_port = os.getenv('DATABASE_PORT',3306)
  database_user = os.getenv('DATABASE_USER',None)
  database_password =  os.getenv('DATBASE_PASSWORD',None)
  flask_port = os.getenv('FLASK_PORT',8080)
  
 


  app.run(debug=True,port=flask_port,host="0.0.0.0") 
