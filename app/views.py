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
					return redirect(request.url)
				else:
					print('confirmed password were wrong')
			else:
				print('no password were sent')
		else:
			print('no user name were sent')

	if method=="POST":
		if "post-title" in form and form["post-title"]:
			if "post-body" in form and form['post-body']:
				post_title = form["post-title"]
				post_body=form["post-body"]
				db=get_db()
				# time=

				db.execute(
					'INSERT INTO posts(title,post) VALUES(?,?)', (post_title, post_body)
				)
				db.commit()
				return redirect(request.url)
			else:
				print("no body were found for thr post")
		else:
			print('no title were found for this post')

	db=get_db()
	users=db.execute('SELECT * FROM users')
	posts=db.execute('SELECT * FROM posts')
	return render_template("home.html"
	,users=users
	,posts=posts
	)
