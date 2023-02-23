from flask import Flask,render_template,redirect,request,session

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
    return render_template('index.html',res='Registered Successfully')

# Create a Route for Login Form
@app.route('/loginform',methods=['post'])
def loginform():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)
    return render_template('index.html',res='Login Valid')


if (__name__=="__main__"):
    app.run(debug=True,port=5001)