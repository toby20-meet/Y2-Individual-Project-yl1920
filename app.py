from flask import Flask, request, redirect, url_for, render_template, request
from flask import session as login_session
from databases import *
import os
from werkzeug import secure_filename
import shutil
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.secret_key = "MY_SUPER_SECRET_KEY"

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connected = False
logins = {'Shalom':'David3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/gallery')
def gallery():
	images = os.listdir('static/images')
	longitude = len(images)
	if longitude%4 == 0:
		portion = longitude/4
		l1 = images[0:portion]
		l2 = images[portion:portion*2]
		l3 = images[portion*2:portion*3]
		l4 = images[portion*3:portion*4]
	else:
		extra = longitude%4
		portion = longitude/4
		l1 = images[0:portion]
		l2 = images[portion:portion*2]
		l3 = images[portion*2:portion*3]
		l4 = images[portion*3:(portion*4+extra)]
	return render_template("gallery.html", images1 = l1,images2 = l2,images3 = l3,images4 = l4)

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/login', methods = ['POST','GET'])
def login():
	global connected
	if connected:
		return redirect(url_for('admin'))
	else:
		if request.method == 'POST':
			if request.form['username'] in logins:
				if logins[request.form['username']] == request.form['pass']:
					connected = True
					return redirect(url_for('admin'))
		return render_template("login.html")

@app.route('/admin', methods = ['POST','GET'])
def admin():
	global connected
	if connected == False:
		return redirect(url_for('login'))
	else:
		if request.method == 'POST':
			if request.form['submition'] == 'add_s':
				student_name = request.form['new_name']
				phone_number = request.form['new_phone_number']
				parent_phone_number = request.form['new_parent_phone_number']
				addStudent(student_name,phone_number,parent_phone_number)
			if request.form['submition'] == 'edit_s':
				change_type = request.form['types']
				new_value = request.form['new_value']
				student_id = request.form['student_id']
				editStudent(student_id,change_type,new_value)
			if request.form['submition'] == 'add_p':
				file = request.files['img[]']
				if file and allowed_file(file.filename):
					print(file)
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			if request.form['submition'] == 'del_p':
				photo_id = request.form['photo_id']
				delPhoto(photo_id)
			if request.form['submition'] == 'del_s':
				student_id = request.form['s_id']
				delStudent(student_id)
		student_names = allStudents()
		photos = all_photos()
		return render_template('admin.html',pn = student_names,pl = photos)

if __name__ == '__main__':
	app.debug = True
	app.run(debug=True)