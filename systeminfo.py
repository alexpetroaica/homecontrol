import subprocess
import os
def get_ram():
	#Returns a tuple (total ram, available ram) in megabytes. See www.linuxatemyram.com
	try:
		s = subprocess.check_output(["free","-m"])
		lines = s.split("\n")       
		return ( int(lines[1].split()[1]), int(lines[2].split()[3]) )
	except:
		return 0 
def get_process_count():
	#Returns the number of processes
	try:
		s = subprocess.check_output(["ps","-e"])
		return len(s.split("\n"))       
	except:
		return 0 
def get_up_stats():
	#Returns a tuple (uptime, 5 min load average)
	try:
		s = subprocess.check_output(["uptime"])
		load_split = s.split("load average: ")
		load_five = float(load_split[1].split(",")[1])
		up = load_split[0]
		up_pos = up.rfind(",",0,len(up)-4)
		up = up[:up_pos].split("up ")[1]
		return ( up , load_five )       
	except:
		return ('' , 0 )
def get_connections():
	#Returns the number of network connections
	try:
		s = subprocess.check_output(["netstat","-tun"])
		return len([x for x in s.split() if x == 'ESTABLISHED'])
	except:
		return 0

def get_temperature():
	#Returns the temperature in degrees C
	try:
		s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
		return float(s.split("=")[1][:-3])
	except:
		return 0

def get_ipaddress():
	#Returns the current IP address
	arg="ip route list"
	p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
	data = p.communicate()
	split_data = data[0].split()
	ipaddr = split_data[split_data.index('src')+1]
	return ipaddr

def get_cpu_speed():
	#Returns the current CPU speed
	f = os.popen("/opt/vc/bin/vcgencmd get_config arm_freq")
	cpu = f.read()
	return cpu

def get_room_temperature():
	#returns the room temperature
	# Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before. 
	tfile = open("/sys/bus/w1/devices/28-000004a215f9/w1_slave") 
	# Read all of the text in the file. 
	text = tfile.read() 
	# Close the file now that the text has been read. 
	tfile.close() 
	# Split the text with new lines (\n) and select the second line. 
	secondline = text.split("\n")[1] 
	# Split the line into words, referring to the spaces, and select the 10th word (counting from 0). 
	temperaturedata = secondline.split(" ")[9] 
	# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number. 
	temperature = float(temperaturedata[2:-2]) 
	# Put the decimal point in the right place and display it. 
	temperature = temperature / 10 
	return temperature
"""


print "Free RAM: "+str(ram[1])+" ("+str(ram[0])+")"
print "Nr. of processes: "+str(get_process_count())
print "Up time: "+get_up_stats()[0]
print "Nr. of connections: "+str(get_connections())
print "Temperature in C: " +str(get_temperature())
print "IP-address: "+get_ipaddress()
print "CPU speed: "+str(get_cpu_speed())
"""