from app import app, datab, models
from flask import render_template, request, redirect

# from app.db import get_db, init_db
from app.models import users
from flask_login import login_user, current_user
import datetime

@app.route('/', methods=['GET', 'POST'])
def get_home():
	form=request.form
	args=request.args
	method=request.method

	if method == "POST":
		# try:
		# 	init_db()
		# except:
		# 	pass

		try:
			datab.create_all()
		except:
			pass
		if "new_username" in form and form['new_username']:
			if "password" in form and form['password']:
				if "c_password" in form and form['c_password'] and form['c_password']==form['password']:
					# db = get_db()
					new_username=form['new_username']
					password=form['password']

					n_user=models.users(
						username=new_username,
						password=password,
					)
					datab.session.add(n_user)
					datab.session.commit()
					login_user(n_user)
					print('user added to users class from models file, and user had been logged in')
					print(current_user)

					# db.execute(
					# 	'INSERT INTO users(username, password) VALUES(?,?)', (new_username,password)
					# )
					# db.commit()
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
				created=datetime.datetime.now().strftime('%B %d %Y - %H:%M')
				# db=get_db()
				# time=

				n_post=models.posts(
					date=created,
					post_title=post_title,
					post_body=post_body,
				)
				datab.session.add(n_post)
				datab.session.commit()
				print('post added to posts class from models file, and post had should be posted')

				# db.execute(
				# 	'INSERT INTO posts(title,post) VALUES(?,?)', (post_title, post_body)
				# )
				# db.commit()
				return redirect(request.url)
			else:
				print("no body were found for thr post")
		else:
			print('no title were found for this post')

	# db=get_db()
	users=models.users.query.all()
	posts=models.posts.query.all()

	return render_template("home.html"
	,users=users
	,posts=posts
	)
