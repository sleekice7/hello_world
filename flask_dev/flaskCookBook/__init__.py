from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from db_connection import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt					#this is for password hashing ans encryption
from MySQLdb import escape_string as thwart				#this is for handling sql injections
import gc												#this module is for handling garbage collection

TOPIC_DICT = Content()

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template("main.html")

@app.route('/dashboard/')
def dashboard():

	flash("Welome to Python CookWeb, lets see how much you can learn!")
	return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
		return render_template("404.html")

@app.route('/login/', methods = ['GET','POST'])
def login_page():
	error = ''
	try:
		c, conn = connection()
		if request.method == "POST":
			data = c.execute("SELECT * FROM users WHERE username = (%s)",
				request.form['username'])
			data = c.fetchone()[2]

			if sha256_crypt.verify(request.form['password'], data):
				session['logged_in'] = True
				session['username'] = request.form['username']

				flash("You are now logged in")
				return redirect(url_for("dashboard"))

			else:
				error = "Invalid Credentials. Please Try Again."

		gc.collect()
		return render_template("login.html", error = error)

	except Exception as e:
		#flash(e)
		error = "Invalid Credentials. Please Try Again."
		return render_template("login.html", error = error)

#Here WTForms allows us to insert validation logic with ease: 
class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	email = TextField('Email Address', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match")])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Notice</a> (Last updated Feb 2020)', [validators.Required()])

@app.route('/register/', methods = ['GET','POST'])
def register_page():
	try:
		form = RegistrationForm(request.form)

		if request.method == "POST" and form.validate():		#if the user interacts with the register/submit button, and the form has been validated, do the following:
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt((str(form.password.data)))
			c, conn = connection()

			x = c.execute("SELECT * FROM users WHERE username = (%s)", (username,))

			if int(x) > 0:
				flash("That name has already been taken, please choose another name")
				return render_template('register.html', form=form)

			else:
				c.execute("INSERT INTO users (username, email, password, tracking) VALUES (%s, %s, %s, %s)",
					(thwart(username), thwart(email), thwart(password), thwart("/introduction-to-python-programming/")))

				conn.commit()				#This line saves the queried data to the database.

				flash("Thanks for registering with us!")
				c.close()
				conn.close()
				gc.collect()

				session['logged_in'] = True				#session helps us track what the user does on the page.
				session['username'] = username

				return redirect(url_for('dashboard'))

		return render_template("register.html", form=form)
		
		#return("Hurray!!!")
	except Exception as e:
		return(str(e))


if __name__ == "__main__":
	app.run()
