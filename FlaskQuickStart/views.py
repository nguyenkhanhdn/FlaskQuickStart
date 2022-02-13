"""
Routes and views for the flask application.
"""

from datetime import datetime
from FlaskQuickStart import app
import pypyodbc #7     
from flask import render_template, redirect, request, url_for,make_response
    
   
# creating connection Object which will contain SQL Server Connection    
conn = pypyodbc.connect('Driver={SQL Server};Server=(local)\\sqlexpress;Database=cms;uid=sa;pwd=123456') #11
# Creating Cursor        
#cursor = conn.cursor()
#cursor.execute("SELECT * FROM EmployeeMaster") 

@app.route("/req")
def req():
    #request.headers.append('key' , 'secret@key!@#@#$$')
    resp = make_response("OK", 200)
    resp.headers['key'] = request.headers['key']
    return resp

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        uname = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        cursor = conn.cursor()
        cursor.execute("insert into accounts(username,email,password) values(?,?,?)",(uname,email,pwd))
        cursor.connection.commit()
        cursor.close()
        return redirect(url_for('home'))

@app.route('/users')
def users():
    cursor = conn.cursor()
    cursor.execute("select * from accounts")
    users = cursor.fetchall() #bang 
    return render_template("users.html",data=users)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        uname = request.form['username']
        pwd = request.form['password']
        cursor = conn.cursor()
        cursor.execute("select * from accounts where username = ? and password = ?",(uname,pwd))
        user = cursor.fetchone()
        if user:
            return "Login thành công"
        else:
            return render_template("login.html",data="Sai tên đăng nhập hoặc mật khẩu.")

@app.route('/edit',methods=['GET','POST'])
def edit():      
    if request.method == 'GET':
        try:
            cursor = conn.cursor()
            sql = "SELECT * FROM accounts WHERE username = ?"
            cursor.execute(sql,(request.args.get("username"),))
            row = cursor.fetchone()
            if row:
                #return render_template('edit.html', row=row)
                return render_template('edit.html', title = "Edit Profile",row = row)
            else:
                return 'Error loading #{id}'.format(id=id)
        except Exception as e:
            return e
        finally:
            cursor.close()
    if request.method == 'POST':
        try:
            u = request.form["username"]
            e = request.form["email"]
            p = request.form["password"]

            cursor = conn.cursor()
            cursor.execute("update accounts set password = ?, email=? where username=?",(p,e,u,))
            cursor.connection.commit()
                #return render_template('edit.html', row=row)
            return "Update successfully."            
        except Exception as e:
            return e
        finally:
            cursor.close()
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

@app.route('/delete',methods = ['GET','POST'])
def delete():
    username = request.args.get("username")
    
    if request.method == 'GET':
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = ?",(username,))
            row = cursor.fetchone()
            if row:
                #return render_template('edit.html', row=row)
                return render_template('deleteconfirm.html', title = "Delete account",row=row)
            else:
                return 'Error loading #{id}'.format(id=id)
        except Exception as e:
            return e
        finally:
            cursor.close()
    if request.method == 'POST':
        try:
            username = request.form["username"]
            cursor = conn.cursor()
            cursor.execute("delete FROM accounts WHERE username = ?",(username,))
            cursor.connection.commit()
            return redirect(url_for('users'))   
        except Exception as e:
            return e
        finally:
            cursor.close()

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
