from flask import Flask,render_template,redirect,request,session
import mysql.connector as mysql
import os
from werkzeug.utils import secure_filename
import hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


db=mysql.connect(
    host='localhost',
    user='root',
    password='',
    database='project17'
)

cur=db.cursor()

# Create APP to launch Web Server
app=Flask(__name__)
app.secret_key='ms17kits'

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

# Create a Route for Upload
@app.route('/upload')
def uploadPage():
    return render_template('upload.html')

# Create a Route for Upload File
@app.route('/uploadFile',methods=['post'])
def uploadFile():
    doc=request.files['chooseFile']
    if session['username'] not in os.listdir():
        os.mkdir(session['username'])
    doc1=secure_filename(doc.filename)
    doc.save(session['username']+'/'+doc1)
    hashvalue=hash_file(session['username']+'/'+doc1)
    sql='INSERT INTO filesdata (username,filename,hash) VALUES (%s,%s,%s)'
    values=(session['username'],session['username']+'/'+doc1,hashvalue)
    cur.execute(sql,values)
    db.commit()
    return render_template('upload.html',res='File Uploaded')

# Create a Route for Sender
@app.route('/sender')
def senderPage():
    if session['username'] in os.listdir():
        k=os.listdir(session['username'])
        print(k)
        data1=[]
        for i in range(len(k)):
            dummy=[]
            dummy.append(k[i])
            data1.append(dummy)
    
    data=[]
    sql='select * from register'
    cur.execute(sql)
    result=cur.fetchall()
    for i in result:
        if(i[1]!=session['username']):
            dummy=[]
            dummy.append(i[1])
            data.append(dummy)
    return render_template('sender.html',l=len(data),l1=len(data1),dashboard_data=data,dashboard_data1=data1)

# Create a Route for senderform
@app.route('/senderform',methods=['post'])
def senderform():
    filename=session['username']+'/'+request.form['filename']
    filehash=hash_file(filename)
    receiver=request.form['receiver']
    print(filename,receiver)
    sql='select * from tokens'
    cur.execute(sql)
    result=cur.fetchall()
    for i in result:
        if(i[4]==receiver and i[3]==filehash):
            if session['username'] in os.listdir():
                k=os.listdir(session['username'])
                print(k)
                data1=[]
                for i in range(len(k)):
                    dummy=[]
                    dummy.append(k[i])
                    data1.append(dummy)
            data=[]
            sql='select * from register'
            cur.execute(sql)
            result=cur.fetchall()
            for i in result:
                if(i[1]!=session['username']):
                    dummy=[]
                    dummy.append(i[1])
                    data.append(dummy)
            return render_template('sender.html',l=len(data),l1=len(data1),dashboard_data=data,dashboard_data1=data1,res1='Already Shared')
    
    sql='INSERT INTO tokens (username,filename,filehash,receivers) VALUES (%s,%s,%s,%s)'
    values=(session['username'],filename,filehash,receiver)
    cur.execute(sql,values)
    db.commit()
    if session['username'] in os.listdir():
        k=os.listdir(session['username'])
        print(k)
        data1=[]
        for i in range(len(k)):
            dummy=[]
            dummy.append(k[i])
            data1.append(dummy)
    data=[]
    sql='select * from register'
    cur.execute(sql)
    result=cur.fetchall()
    for i in result:
        if(i[1]!=session['username']):
            dummy=[]
            dummy.append(i[1])
            data.append(dummy)
    
    return render_template('sender.html',l=len(data),l1=len(data1),dashboard_data=data,dashboard_data1=data1,res='Shared')

# Create a Route for Sent
@app.route('/sent')
def sent():
    sql='select * from tokens'
    cur.execute(sql)
    result=cur.fetchall()
    data=[]
    for i in result:
        if(i[1]==session['username']):
            dummy=[]
            dummy.apend(i[4])
            dummy.append(i[2])
            dummy.append(i[3])
            data.append(dummy)
    
    return render_template('sent.html',dashboard_data=data,l=len(data))

# Create a Rotue for Logout
@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

if (__name__=="__main__"):
    app.run(debug=True,port=5001)