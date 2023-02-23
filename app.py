from flask import Flask,render_template,redirect,request,session
import mysql.connector as mysql
import json

app=Flask(__name__)
db=mysql.connect(
    host='localhost',
    user='root',
    password='',
    database='project17'
)

cur=db.cursor()

# Create APP to launch Web Server
app=Flask(__name__)

# Create a Route to Register
@app.route('/')
def registerPage():
    return render_template('index.html')

# Create a Route for Register Form
@app.route('/signupform',methods=['post'])
def signupform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    try:
        sql='INSERT INTO register (username,password) VALUES (%s,%s)'
        values=(username,password)
        cur.execute(sql,values)
        db.commit()
        return render_template('index.html',res='Registered Successfully')
    except:
        return render_template('index.html',err='Register Failed')

# Create a Route for Login Form
@app.route('/loginform',methods=['post'])
def loginform():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)

    sql='select * from register'
    cur.execute(sql)
    result=cur.fetchall()
    data=[]
    for i in result:
        data.append(i)
    print (json.dumps(data))
    return render_template('index.html',res='Login Valid')


if (__name__=="__main__"):
    app.run(debug=True,port=5001)