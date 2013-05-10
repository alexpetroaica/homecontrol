from flask import Flask, render_template, redirect, request, session, url_for, escape
from lirc import Lirc
import systeminfo
app = Flask(__name__) 
 
# Initialise the Lirc config parser
lircParse = Lirc('/etc/lirc/lircd.conf')

@app.route("/")  
def hello():
	if 'username' in session:
		#the user is logged in, display everything
		return render_template('home.html', username=session['username'],ram=systeminfo.get_ram(),processes=systeminfo.get_process_count(),sysTemp=systeminfo.get_temperature(),roomTemp=systeminfo.get_room_temperature())
	else:
		return redirect("/login")
	
@app.route("/login", methods=['GET', 'POST'])  
def login():
	global current_user
	#GET
	if request.method == 'GET':
		if 'username' in session:
			#the user is logged in, redirect to home
			return redirect("/")
		else:
			return render_template('login.html')
	#POST		
	elif request.method == 'POST':
		if request.form['username']=="admin" and request.form['password']=="nevada70":
			session['username'] = request.form['username']
			return redirect("/")

@app.route("/logout")  
def logout():
	#remove the username from the session if it's there
	session.pop('username', None)
	return redirect("/login")

@app.route("/remotes")
def remotes():
	if 'username' in session:
		# Get the devices from the config file
		devices = []
		for dev in lircParse.devices():
			d = {
				'id': dev,
				'name': dev,
			}
			devices.append(d)
		
		return render_template('remotes.html', devices=devices,username=session['username'])
	else:
		return redirect("/login")


@app.route("/remotes/<device_id>/clicked/<op>")
def clicked(device_id=None, op=None):
	
	if 'username' in session:
		# Send message to Lirc to control the IR
		lircParse.send_once(device_id, op)
		
		return ""
	else:
		return redirect("/login")


@app.route("/actions/dim-bedroom-lights")
def dimBedroomLights():
	if 'username' in session:
		# Send message to Lirc to simulate large remote
		lircParse.send_twenty_times("Bedroom-Ambiental", "KEY_BRIGHTNESS_DOWN")
		
		return ""
	else:
		return redirect("/login")

@app.route("/actions/fullpower-bedroom-lights")
def fullPowerBedroomLights():
	if 'username' in session:
		# Send message to Lirc to simulate large remote
		lircParse.send_twenty_times("Bedroom-Ambiental", "KEY_BRIGHTNESS_UP")
		
		return ""
	else:
		return redirect("/login")

if __name__ == "__main__":  
	app.secret_key = 'A0Fr94j/3yX F~XOH!jmN]LWX/,?RT'
	app.debug = True
	
	app.run('0.0.0.0',80) 