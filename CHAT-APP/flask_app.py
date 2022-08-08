import json
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template,request, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'} 
db = SQLAlchemy(app)

class Chat(db.Model): 
    __bind_key__ = 'chat'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def __repr__(self):
	    return f"{self.username} email is {self.email} and password is {self.password}"

@app.route("/") 
def default():
    return redirect(url_for('login_controller'))

@app.route("/login/", methods=["GET","POST"]) 
def login_controller(): 
    if request.method == "POST":
        password = request.form['password']
        name = request.form['user_name']
        table_info = User.query.filter_by(username=name).first()
        if table_info == None:
            return redirect(url_for('register_controller'))
        passwords = table_info.password
        if passwords == password:
            return redirect(url_for('profile',username=name))
        else:
            return render_template('loginPage.html')
    return render_template('loginPage.html')

@app.route("/register/", methods=["GET", "POST"]) 
def register_controller(): 
    if request.method == "POST":
        password = request.form['new_password']
        con_password = request.form['confirmed_password']
        if password == con_password:
            name = request.form['new_user_name']
            if name!="" and password!="":
                if User.query.filter_by(username=name).first()!=None:
                    print("The username already exist!")
                    return render_template('register.html')
                a_new_user = User(username=name,password=password,email=request.form['email'])
                try:
                    db.session.add(a_new_user)
                    db.session.commit()
                    return redirect(url_for('profile',username = name))
                except:
                    return f'<h1>There was an issue!</h1>'
            else:
                print("Username or password can not be empyt!")
        else:
            print("Password are not the same! Enter new one")
            return render_template('register.html')
    return render_template('register.html')

@app.route("/profile/<username>") 
def profile(username=None): 
    return render_template('chat_page.html', name=username)

@app.route("/logout/") 
def unlogger(): 
    return render_template('logoutPage.html')

@app.route("/new_message/", methods=["POST"]) 
def new_message(): 
    the_new_message = Chat(username=request.form["username"],message=request.form["message"])
    db.session.add(the_new_message)
    db.session.commit()
    return redirect(url_for('profile',username = request.form["username"]))
   
@app.route("/messages/") 
def messages(): 
    res = []
    all_chat = Chat.query.order_by(desc(Chat.id)).all() 
    for chat in all_chat:
        new_elem = [chat.username,chat.message]
        res.append(new_elem)
    return json.dumps(res)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
