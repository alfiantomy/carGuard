'''
Created on Sep 22, 2017

@author: Tomy
'''

#import RPi.GPIO as GPIO
import MySQLdb
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import time
import urllib2, urllib

'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(17, True)
GPIO.output(18, False)
'''

######################################################################
### FUNGSI IMPORT DB - START #########################################
#====================================================================#
def importflag():
	## IMPORT FLAG
	url = r'http://carguard.000webhostapp.com/ImportFlag.php'
	flag = urllib2.urlopen(url).read()
	#remote_data = json.load(response)
	print flag

def importcounter():
	## IMPORT MODE COUNTER
	url = r'http://carguard.000webhostapp.com/ImportCounter.php'
	counter = urllib2.urlopen(url).read()
	#remote_data = json.load(response)
	print counter
#====================================================================#
### FUNGSI IMPORT DB - END ###########################################
######################################################################
	
	
	
######################################################################
### FUNGSI MAIN - START ##############################################
#====================================================================#
def main():
	"""	
	## RELAY START
	sqlRelay = "select * from relay where id = '%s'" %(1)
	cur.execute(sqlRelay)
	resultRelay = cur.fetchall()
	for row in resultRelay:
		relay_finger = row[2]

	sqlRelay = "select * from relay where id = '%s'" %(2)
	cur.execute(sqlRelay)
	resultRelay = cur.fetchall()
	for row in resultRelay:
		relay_alarm = row[2]
		
	if relay_finger == 1:
		GPIO.output(17, True)
		pass
	elif relay_finger == 0:
		GPIO.output(17, False)
		pass
	if relay_alarm == 1:
		GPIO.output(18, True)
		pass
	elif relay_alarm == 0:
		GPIO.output(18, False)
		pass
	## RELAY END
	"""
	## FLAG START
	url = r'http://carguard.000webhostapp.com/ImportFlag.php'
	flag = urllib2.urlopen(url).read()	
	print flag
	
	if flag == '100000':
		mode()
	elif flag == '010000':
		speed()
	elif flag == '001000':
		alarm()
	elif flag == '000100':
		finger()
	elif flag == '000010':
		new_finger()
	elif flag == '000001':
		del_finger()
	else:
		pass
	## FLAG END
#====================================================================#
### FUNGSI MAIN - END ################################################
######################################################################


######################################################################
########## FUNGSI MODE - START #######################################
#====================================================================#
def mode():
	url = r'http://carguard.000webhostapp.com/ImportCounter.php'
	counter = urllib2.urlopen(url).read()
	print counter[0]
	mode_counter = counter[0]
	
	if mode_counter == 1:
		#V Ubah fingercount = 1
		myUpdate=[('code', 'mode1')]
		myUpdate=urllib.urlencode(myUpdate)
		path='http://carguard.000webhostapp.com/update.php'
		req=urllib2.Request(path, myUpdate)
		page=urllib2.urlopen(req).read()
		print page
		finger()

	elif mode_counter == 0:
		#V Ubah fingercount = 0
		myUpdate=[('code', 'mode0')]
		myUpdate=urllib.urlencode(myUpdate)
		path='http://carguard.000webhostapp.com/update.php'
		req=urllib2.Request(path, myUpdate)
		page=urllib2.urlopen(req).read()
		print page
		
	#V modeflag = 0 ## Update database
	myUpdate=[('code', 'mode')]
	myUpdate=urllib.urlencode(myUpdate)
	path='http://carguard.000webhostapp.com/update.php'
	req=urllib2.Request(path, myUpdate)
	page=urllib2.urlopen(req).read()
	print page
#====================================================================#
########## FUNGSI MODE - END #########################################
######################################################################


######################################################################
########## FUNGSI SPEED - START ######################################
#====================================================================#
def speed():
	url = r'http://carguard.000webhostapp.com/ImportCounter.php'
	counter = urllib2.urlopen(url).read()
	print counter[1]
	speed_counter = counter[1]
	
	if speed_counter == '1':
		#mekanik_speed = 1 # Ayo ndang dibuat
		pass
	elif speed_counter == '0':
		#mekanik_speed = 0 # Ayo ndang dibuat
		pass
		
	#V speedflag = 0 ## Update database
	myUpdate=[('code', 'speed')]
	myUpdate=urllib.urlencode(myUpdate)
	path='http://carguard.000webhostapp.com/update.php'
	req=urllib2.Request(path, myUpdate)
	page=urllib2.urlopen(req).read()
	print page
#====================================================================#
########## FUNGSI SPEED - END ########################################
######################################################################

	
######################################################################
########## FUNGSI ALARM - START ######################################
#====================================================================#
def alarm():
	url = r'http://carguard.000webhostapp.com/ImportCounter.php'
	counter = urllib2.urlopen(url).read()
	print counter[2]
	alarm_counter = counter[2]
	
	if alarm_counter == '1':
		myUpdate=[('code', 'alarm1')]
		myUpdate=urllib.urlencode(myUpdate)
		path='http://carguard.000webhostapp.com/update.php'
		req=urllib2.Request(path, myUpdate)
		page=urllib2.urlopen(req).read()
		print page
		#GPIO.output(18, True)
	elif alarm_counter == '0':
		myUpdate=[('code', 'alarm0')]
		myUpdate=urllib.urlencode(myUpdate)
		path='http://carguard.000webhostapp.com/update.php'
		req=urllib2.Request(path, myUpdate)
		page=urllib2.urlopen(req).read()
		print page
		#GPIO.output(18, False)
		
	#V alarmflag = 0 ## Update database
	myUpdate=[('code', 'alarm')]
	myUpdate=urllib.urlencode(myUpdate)
	path='http://carguard.000webhostapp.com/update.php'
	req=urllib2.Request(path, myUpdate)
	page=urllib2.urlopen(req).read()
	print page
#====================================================================#
########## FUNGSI ALARM - END ########################################
######################################################################


######################################################################
########## FUNGSI SCAN FINGER - START ################################
#====================================================================#
def finger():
	url = r'http://carguard.000webhostapp.com/ImportCounter.php'
	counter = urllib2.urlopen(url).read()
	print counter[3]
	finger_counter = counter[3]
	
	if finger_counter == '1':
		#GPIO.output(17, True)
		myUpdate=[('code', 'finger1')]
		myUpdate=urllib.urlencode(myUpdate)
		path='http://carguard.000webhostapp.com/update.php'
		req=urllib2.Request(path, myUpdate)
		page=urllib2.urlopen(req).read()
		print page
		need_finger()
	elif finger_counter == '0':
		#GPIO.output(17, False)
		myUpdate=[('code', 'finger0')]
		myUpdate=urllib.urlencode(myUpdate)
		path='http://carguard.000webhostapp.com/update.php'
		req=urllib2.Request(path, myUpdate)
		page=urllib2.urlopen(req).read()
		print page
	
	#V fingerflag == 0 ## Update database
	myUpdate=[('code', 'finger')]
	myUpdate=urllib.urlencode(myUpdate)
	path='http://carguard.000webhostapp.com/update.php'
	req=urllib2.Request(path, myUpdate)
	page=urllib2.urlopen(req).read()
	print page
	start()

def need_finger():
	## Scan and Search for a finger
	##
	## Tries to initialize the sensor
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')

	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		exit(1)
	
	## Gets some sensor information
	print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
		
	## Tries to search the finger and calculate hash
	while True:
		
	##	try:  ### Cek di file fingerprint yang asli apa kegunaan "try"???
		print('Waiting for finger...')
	
		## Wait that finger is read
		while ( f.readImage() == False ):			
			url = r'http://carguard.000webhostapp.com/ImportCounter.php'
			counter = urllib2.urlopen(url).read()
			print counter[3]
			finger_counter = counter[3]
		
			if finger_counter == 0:
				#GPIO.output(17, False)
				myUpdate=[('code', 'finger0')]
				myUpdate=urllib.urlencode(myUpdate)
				path='http://carguard.000webhostapp.com/update.php'
				req=urllib2.Request(path, myUpdate)
				page=urllib2.urlopen(req).read()
				print page
				start()
			main()

		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)
	
		## Searchs template
		result = f.searchTemplate()
	
		positionNumber = result[0]
		accuracyScore = result[1]
	
		## Result
		if (positionNumber == -1):
			print('No match found!')
		else:
			print('Found template at position #' + str(positionNumber))
			print('The accuracy score is: ' + str(accuracyScore))
			myUpdate=[('code', 'fingerV')]
			myUpdate=urllib.urlencode(myUpdate)
			path='http://carguard.000webhostapp.com/update.php'
			req=urllib2.Request(path, myUpdate)
			page=urllib2.urlopen(req).read()
			print page
			finger()
			#start()
#====================================================================#
########## FUNGSI SCAN FINGER - END ##################################
######################################################################


######################################################################
########## FUNGSI NEW FINGER - START #################################
#====================================================================#
def new_finger():
	## Enrolls new finger
	##
	## Tries to initialize the sensor
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
	
	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		new_finger()
	
	## Gets some sensor information
	print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
	
	## Tries to enroll new finger
	try:
		print('Waiting for finger...')
	
		## Wait that finger is read
		while ( f.readImage() == False ):
			url = r'http://carguard.000webhostapp.com/ImportFlag.php'
			flag = urllib2.urlopen(url).read()
			print flag[5]
			new_finger_flag = flag[5]
		
			if new_finger_flag == 0:
				start()
			#main()

		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)
	
		## Checks if finger is already enrolled
		result = f.searchTemplate()
		positionNumber = result[0]
	
		if ( positionNumber >= 0 ):
			print('Template already exists at position #' + str(positionNumber))
			new_finger()
	
		print('Remove finger...')
		time.sleep(1)
	
		print('Waiting for same finger again...')
	
		## Wait that finger is read again
		while ( f.readImage() == False ):
			url = r'http://carguard.000webhostapp.com/ImportFlag.php'
			flag = urllib2.urlopen(url).read()
			print flag[5]
			new_finger_flag = flag[5]
		
			if new_finger_flag == 0:
				start()
			#main()

		## Converts read image to characteristics and stores it in charbuffer 2
		f.convertImage(0x02)
	
		## Compares the charbuffers
		if ( f.compareCharacteristics() == 0 ):
			raise Exception('Fingers do not match')
	
		## Creates a template
		f.createTemplate()
	
		## Saves template at new position number
		positionNumber = f.storeTemplate()
		print('Finger enrolled successfully!')
		print('New template position #' + str(positionNumber))
	
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		new_finger()

	finger_info_update()
	#V newfingerflag == 0 ## Update database
	myUpdate=[('code', 'newfinger')]
	myUpdate=urllib.urlencode(myUpdate)
	path='http://carguard.000webhostapp.com/update.php'
	req=urllib2.Request(path, myUpdate)
	page=urllib2.urlopen(req).read()
	print page
	start()
#====================================================================#
########## FUNGSI NEW FINGER - END ###################################
######################################################################


######################################################################
########## FUNGSI NEW FINGER - START #################################
#====================================================================#
def del_finger():
	## Deletes a finger from sensor
	##
	## Tries to initialize the sensor
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
	
	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		exit(1)
	
	## Gets some sensor information
	print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
	
	## Tries to delete the template of the finger
	try:
		tableIndex = f.getTemplateIndex(0)
		for i in range(0, 5):
			print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))		
	
		url = r'http://carguard.000webhostapp.com/finger_del_value.php'
		del_finger_template = urllib2.urlopen(url).read()	
		print del_finger_template
		del_finger_template = int(del_finger_template)
		positionNumber = del_finger_template
		
		if ( f.deleteTemplate(positionNumber) == True ):
			print('Template deleted!')

	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		exit(1)

	finger_info_update()
	#V delfingerflag == 0 ## Update database
	myUpdate=[('code', 'delfinger')]
	myUpdate=urllib.urlencode(myUpdate)
	path='http://carguard.000webhostapp.com/update.php'
	req=urllib2.Request(path, myUpdate)
	page=urllib2.urlopen(req).read()
	print page
	start()
#====================================================================#
########## FUNGSI NEW FINGER - END ###################################
######################################################################


######################################################################
########## FUNGSI FINGER INFO - START ##################################
#====================================================================#
def finger_info_update():
	## Tries to initialize the sensor
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
	
	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		exit(1)
	
	## Send sensor information
	used = int(f.getTemplateCount())
	
	tableIndex = f.getTemplateIndex(0)
	index={}
	for i in range(0, 5):
		index[i] = int(tableIndex[i])
		#print index[i]
	myfingertemplatestatus=[('used', used), ('fingertemplate', index)] #('var_name', value)
	myfingertemplatestatus=urllib.urlencode(myfingertemplatestatus)
	path='http://carguard.000webhostapp.com/tes3.php'    #the url you want to POST to
	req=urllib2.Request(path, myfingertemplatestatus)
	page=urllib2.urlopen(req).read()
	print page
		
#====================================================================#
### FUNGSI FINGER INFO - END #########################################
######################################################################

def start():
	while 1:
		main()

######################################################################
########## START #####################################################
#====================================================================#
start()
#====================================================================#
########## END #######################################################
######################################################################
	

