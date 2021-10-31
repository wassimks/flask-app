from app import app 
from flask import render_template, request, redirect

from app.db import get_db, init_db

@app.route('/', methods=['GET', 'POST'])
def get_home():
	form=request.form
	args=request.args
	method=request.method

	if method == "POST":
		try:
			init_db()
		except:
			pass
		if "new_username" in form and form['new_username']:
			if "password" in form and form['password']:
				if "c_password" in form and form['c_password'] and form['c_password']==form['password']:
					db = get_db()
					new_username=form['new_username']
					password=form['password']

					db.execute(
						'INSERT INTO users(username, password) VALUES(?,?)', (new_username,password)
					)
					db.commit()
					users=db.execute(
						'SELECT * FROM users'
					)
					for user in users:
						print(user[1])
					return redirect(request.url)
				else:
					print('confirmed password were wrong')
			else:
				print('no password were sent')
		else:
			print('no user name were sent')

	return render_template("home.html")


