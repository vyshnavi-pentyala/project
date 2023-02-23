from flask import Flask,render_template,redirect,request,session
import mysql.connector as mysql
import json

app=Flask(__name__)
app.secret_key='ms17kits'

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
        sql='select * from register'
        cur.execute(sql)
        result=cur.fetchall()
        for i in result:
            if username==i[1]:
                return render_template('index.html',res1='User Exist')

        sql='INSERT INTO register (username,password) VALUES (%s,%s)'
        values=(username,password)
        cur.execute(sql,values)
        db.commit()
        return render_template('index.html',res='Registered Successfully')
    except:
        return render_template('index.html',res1='Register Failed')

# Create a Route for Login Form
@app.route('/loginform',methods=['post'])
def loginform():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)

    sql='select * from register'
    cur.execute(sql)
    result=cur.fetchall()
    for i in result:
        if username==i[1] and password==i[2]:
            session['username']=username
            return redirect('/dashboard')
    
    return render_template('index.html',res1='Invalid credentials')

# Create a Route for Dashboard
@app.route('/dashboard')
def dashboardPage():
    return render_template('dashboard.html')

if (__name__=="__main__"):
    app.run(debug=True,port=5001)