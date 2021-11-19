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

	print('[Create account] >>')
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

	print('[Login] >>')
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

	print('[Create post] >>')
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
	
	print('[Edite form] >>')
	if 'edited_post' in form and form['edited_post']:
		new= form['edited_post']
		id= form['edited-post-id']
		edited_post(new, id)
		return redirect(request.url)

	print('[Delete post] >>')
	if 'delete_post' in args and args['delete_post']:
		id= args['delete_post']
		delete_post(id)
		return redirect(request.url_root)

	print('[Add Comment] >>')
	if 'add-comment' in form and form['add-comment']:
		comment= form['add-comment']
		commenter= form['commenter']
		time_of_comment= datetime.datetime.now().strftime('%B %d %Y - %H:%M')
		origin= form['original_post']

		new_comment= models.comments(
			date= time_of_comment,
			commenter= commenter,
			original_post=origin,
			c_content=comment			
		)

		datab.session.add(new_comment)
		datab.session.commit()
		print('comment added')
		return redirect(request.url)
	
	print('[Add mark] >>')
	if 'note_to_send' in form and request.form['note_to_send']:
		print('note do exicte')
		if 'user_id' in form and form['user_id']:
			mark=form['note_to_send']
			user_id=form['user_id']
			post_id=form['post_id']

			new_mark= models.marks(
				mark=mark,
				relative_user_id= user_id,
				relative_post_id= post_id,
			)
			datab.session.add(new_mark)
			datab.session.commit()
			return redirect(request.url)
	else:
		print('note not recieved ;'+ method)
		print(form)
	
	base=sqlite3.connect('app/alchemy.db')
	curs=base.cursor()


	users=models.users.query.all()
	marks=models.marks.query.all()
	posts=curs.execute(
		'SELECT * FROM posts ORDER BY id DESC'
	).fetchall()
	base.commit()
	base.close()
	comments= models.comments.query.all()

	all_avrgs=[]
	try:
		for post in posts:
			s_avrg=calclate_post_average(id=post[0])
			all_avrgs.append(s_avrg)
			base=sqlite3.connect('app/alchemy.db')
			curs=base.cursor()
			curs.execute(
				'UPDATE posts SET average_mark=(?) WHERE id=(?)', (s_avrg, post[0])
			)
			base.commit()
			base.close()
	except:
		pass
	print(all_avrgs)

	try:
		count=count_coins(id=current_user.id, data=posts)
	except:
		count="???"

	return render_template("home.html"
	,users=users
	,posts=posts
	,admin=admin
	,comments=comments
	,all_avrgs=all_avrgs
	,marks=marks
	,test=test
	,count=count
	)

@app.route('/123/<post_id>')
def tryit(post_id):
	print(calclate_post_average(id=post_id))
	return

@app.route('/register')
def get_register():
	return render_template('ph_register.html')

@app.route('/login', methods=['GET','POST'])
def get_login():
	form=request.form
	if request.method=='POST':
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
						return redirect(request.url_root)
					else:
						print('wrong password were given')
				else:
					print('no user with the specified username were found')
			else:
				print('no password to login or wrong password')
		else :
			print('no username sent to login or wrong username')
		return redirect(request.url_root)
	return render_template('ph_login.html')

@app.route('/logout')
def out():
	logout_user()
	return redirect(url_for('get_home'))

@app.route('/posting', methods=['GET','POST'])
def get_posting():
	method=request.method
	form=request.form

	print('get_postin route >>')
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
				return redirect(request.url_root)
			else:
				print("no body were found for thr post")
		else:
			print('no title were found for this post')
	else:
		print('method not equal to post '+" ; "+ method)

	return render_template('ph_posting.html')


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

def calclate_post_average(id):
	db = sqlite3.connect('app/alchemy.db')
	curs = db.cursor()

	marks=curs.execute(
		'SELECT mark FROM marks WHERE relative_post_id=(?)',(id,) 
	).fetchall()
	db.close()
	all=[]
	for mark in marks:
		all.append(mark[0])

	x=0
	total=0
	while x<len(all):
		total+=all[x]
		x +=1
	else:
		avrg=float("{:.2f}".format(total/int(len(all))))

	return avrg

def test(inp):
	stat=0
	try:
		marks=models.marks.query.filter_by(relative_user_id=current_user.id).all()
		for mark in marks:
			if inp == mark.relative_post_id:
				stat=1
				break
	except:
		pass
	return stat

def count_coins(id, data):
	count=0
	try:
		for row in data:
			if id==row[4]:
				count+=row[5]*100
	except:
		print('not functioning')
	return format(count, ".2f")