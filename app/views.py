from flask.helpers import url_for
from flask_login.utils import login_required, logout_user
from app import app, datab, models
from flask import render_template, request, redirect, current_app
import sqlite3

# from app.db import get_db, init_db
from app.models import users
from flask_login import login_user, current_user
import datetime

@app.route('/', methods=['GET', 'POST'])
def get_home():
	form=request.form
	args=request.args
	method=request.method
	admin=''

	if method == "POST":
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

	if method == "POST":
		try:
			datab.create_all()
		except:
			pass
		# print('1st step')
		if "username_to_login" in form and form['username_to_login']:
			# print('2nd step')
			if "password_to_login" in form and form['password_to_login']:
				username_to_check=form['username_to_login']
				password_to_check=form['password_to_login']

				user_found=models.users.query.filter_by(username=username_to_check).first()
				if user_found and user_found.username :
					if user_found.password==password_to_check:
						login_user(user_found)
						return redirect(request.url)
					else:
						print('wrong password were given')
				else:
					print('no user with the specified username were found')
			else:
				print('no password to login or wrong password')
		else :
			print('no username sent to login or wrong username')

	if method == "POST":
		# print('first step to post validated ')
		if "post-title" in form and form["post-title"]:
			# print('second step to post validated ')
			if "post-body" in form and form['post-body']:
				# print('third step to post validated ')
				post_title = form["post-title"]
				post_body=form["post-body"]
				created=datetime.datetime.now().strftime('%B %d %Y - %H:%M')
				# db=get_db()
				# time=

				n_post=models.posts(
					date=created,
					post_title=post_title,
					post_body=post_body,
					relative_index=current_user.id
				)
				datab.session.add(n_post)
				datab.session.commit()
				print('post added to posts class from models file, and post had should be posted')
				return redirect(request.url)
			else:
				print("no body were found for thr post")
		else:
			print('no title were found for this post')
	else:
		print('method not equal to post '+" ; "+ method)
	
	if 'edited_post' in form and form['edited_post']:
		new= form['edited_post']
		id= form['edited-post-id']
		edited_post(new, id)
		return redirect(request.url)

	if 'delete_post' in args and args['delete_post']:
		id= args['delete_post']
		delete_post(id)
		return redirect(request.url_root)

	users=models.users.query.all()
	posts=models.posts.query.all()

	return render_template("home.html"
	,users=users
	,posts=posts
	,admin=admin
	)

@app.route('/logout')
def out():
	logout_user()
	return redirect(url_for('get_home'))


""" @app.route('/edit')
def edit():
	args=request.args
	id=args['edit']
	post=get_post(id)
	return post
 """

def get_post(id):
	# db=models.posts.query.filter_by(id=id).first()
	db = sqlite3.connect('app/alchemy.db')
	curs = db.cursor()

	post=curs.execute(
		'SELECT post_body, post_title FROM posts WHERE id=(?)',(id,) 
	).fetchone()
	db.close()
	return post

def edited_post(new_body, id):
	db=sqlite3.connect('app/alchemy.db')
	curs=db.cursor()
	curs.execute(
		'UPDATE posts SET post_body=(?) WHERE id=(?)', (new_body, id)
	)

	db.commit()
	db.close()
	print('post should been edited')
	
def delete_post(id):
	db=sqlite3.connect('app/alchemy.db')
	curs=db.cursor()
	curs.execute(
		' DELETE FROM posts WHERE id=(?)', (id,)
	)

	db.commit()
	db.close()
	print('post should been edited')
