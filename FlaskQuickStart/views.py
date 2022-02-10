"""
Routes and views for the flask application.
"""

from datetime import datetime
from FlaskQuickStart import app
import pypyodbc      
from flask import render_template, redirect, request, url_for    
   
# creating connection Object which will contain SQL Server Connection    
conn = pypyodbc.connect('Driver={SQL Server};Server=.\\sqlexpress;Database=cms;uid=sa;pwd=123456')
# Creating Cursor        
#cursor = conn.cursor()
#cursor.execute("SELECT * FROM EmployeeMaster") 


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        uname = request.form['username'];
        email = request.form['email'];
        pwd = request.form['password'];
        cursor = conn.cursor()
        cursor.execute("insert into accounts(username,email,password) values(?,?,?)",(uname,email,pwd))
        cursor.connection.commit()
        cursor.close()
        return redirect(url_for('home'))

@app.route('/users')
def users():
    cursor = conn.cursor()
    cursor.execute("select * from accounts")
    users = cursor.fetchall()
    return render_template("users.html",data=users)

@app.route('/profile/<username>')
def profile(username):
    if username == None:
        return redirect(url_for('users'))
    if request.method == 'GET':
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = ?",(username,))
            row = cursor.fetchone()
            if row:
                #return render_template('edit.html', row=row)
                return render_template('profile.html', title = "Profile",heading="Account profile",row=row)
            else:
                return 'Error loading #{id}'.format(id=id)
        except Exception as e:
            return e
        finally:
            cursor.close()
    
@app.route('/edit/<username>')
def edit(username):
    return f"edit {username}"

@app.route('/delete/<username>')
def delete(username):
    return f"delete {username}"


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
