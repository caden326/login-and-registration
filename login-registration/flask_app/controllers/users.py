from flask_app.models.user import User
from flask_app import app
from flask import  render_template, request, redirect, session

# from flask_app.models.user import User

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

from flask import flash




@app.route('/')
def index():

    return redirect ('/login_or_register')

@app.route('/login_or_register')
def show():
    return render_template('index.html')



@app.route('/register', methods=['POST'] )
def register():
    if not User.validate_registration(request.form):
        return redirect('/')

    data1 = {
        'email' : request.form['email']
    }

    if User.get_by_email(data1):
        flash('email already exists')
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name':request.form["first_name"],
        'last_name':request.form["last_name"],
        'email':request.form["email"],
        'password': pw_hash
    }

    new_user_id = User.save(data)
    session["user_id"] = new_user_id
    return redirect("/success")






@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/success")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login_or_register')
    


@app.route('/success')
def success():
    if "user_id" not in session:
        flash("please login or register")
        return redirect('/')

    data = {
        "id" : session["user_id"]
    }

    logged_user = User.user_info(data)
    return render_template('showuser.html', users = logged_user)