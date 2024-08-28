'''
Created on Sep 22, 2017

@author: Tomy
'''

#import RPi.GPIO as GPIO
import MySQLdb
#import hashlib
#from pyfingerprint.pyfingerprint import PyFingerprint
import time

######################################################################
########## FUNGSI MODE - START #######################################
#====================================================================#
def mode():
	con = MySQLdb.connect("localhost", "root", "", "test")
	cur = con.cursor()
	sqlMode = "select * from counter where var = '%s'" %("modecount")
	cur.execute(sqlMode)
	resultMode = cur.fetchall()

	for row in resultMode:
		index = row[0]
		fmodecount = row[1]
		mode_counter = row[2]
	print(mode_counter)
	if mode_counter == 1:
		#V Ubah fingercount = 1
		sqlFingerCount = "UPDATE counter SET counter = 1 WHERE var = 'fingercount'"
		cur.execute(sqlFingerCount)
		con.commit()
		need_finger() # ditinjau lagi ini
		# Ubah relay_finger = 0
		
	elif mode_counter == 0:
		#V Ubah fingercount = 0
		sqlFingerCount = "UPDATE counter SET counter = 0 WHERE var = 'fingercount'"
		cur.execute(sqlFingerCount)
		con.commit()
		# Ubah relay_finger = 1
        
	#V modeflag = 0 ## Update database
	sqlMode = "UPDATE flag SET flag = 0 WHERE fungsi = 'modeflag'"
	cur.execute(sqlMode)
	con.commit()
#====================================================================#
########## FUNGSI MODE - END #########################################
######################################################################

######################################################################
########## FUNGSI SPEED - START ######################################
#====================================================================#
def speed():
	con = MySQLdb.connect("localhost", "root", "", "test")
	cur = con.cursor()
	sqlSpeed = "select * from counter where var = '%s'" %("speedcount")
	cur.execute(sqlSpeed)
	resultSpeed = cur.fetchall()

	for row in resultSpeed:
		index = row[0]
		fspeedcount = row[1]
		speed_counter = row[2]
    
	if speed_counter == 1:
		#mekanik_speed = 1 # Ayo ndang dibuat
		pass
	elif speed_counter == 0:
		#mekanik_speed = 0 # Ayo ndang dibuat
		pass
        
	#V speedflag = 0 ## Update database
	sqlSpeed = "UPDATE flag SET flag = 0 WHERE fungsi = 'speedflag'"
	cur.execute(sqlSpeed)
	con.commit()
#====================================================================#
########## FUNGSI SPEED - END ########################################
######################################################################
	
######################################################################
########## FUNGSI ALARM - START ######################################
#====================================================================#
def alarm():
	con = MySQLdb.connect("localhost", "root", "", "test")
	cur = con.cursor()
	sqlAlarm = "select * from counter where var = '%s'" %("alarmcount")
	cur.execute(sqlAlarm)
	resultAlarm = cur.fetchall()

	for row in resultAlarm:
		index = row[0]
		falarmcount = row[1]
		alarm_counter = row[2]
    
	if alarm_counter == 1:
		relay_alarm = 1
	elif alarm_counter == 0:
		relay_alarm = 0
        
	#V alarmflag = 0 ## Update database
	sqlAlarm = "UPDATE flag SET flag = 0 WHERE fungsi = 'alarmflag'"
	cur.execute(sqlAlarm)
	con.commit()
#====================================================================#
########## FUNGSI ALARM - END ########################################
######################################################################

######################################################################
########## FUNGSI SCAN FINGER - START ################################
#====================================================================#
def finger():
	con = MySQLdb.connect("localhost", "root", "admin", "tes")
	cur = con.cursor()
	sqlFinger = "select * from counter where var = '%s'" %("fingercount")
	cur.execute(sqlFinger)
	resultFinger = cur.fetchall()

	for row in resultFinger:
		index = row[0]
		ffingercount = row[1]
		finger_counter = row[2]
    
	if finger_counter == 1:
		relay_finger = 0
		need_finger()
	elif finger_counter == 0:
		relay_finger = 1
    
	#V fingerflag == 0 ## Update database
	sqlFinger = "UPDATE flag SET flag = 0 WHERE fungsi = 'fingerflag'"
	cur.execute(sqlFinger)
	con.commit()

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
			pass

		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)

		## Searchs template
		result = f.searchTemplate()

		positionNumber = result[0]
		accuracyScore = result[1]

		## Result
		if (positionNumber == -1):
			print('No match found!')
			#GPIO.output(17, False) # Tentukan mau ubah relay dari database atau langsung GPIO
		else:
			print('Found template at position #' + str(positionNumber))
			print('The accuracy score is: ' + str(accuracyScore))
			sqlFingerCount = "UPDATE counter SET counter = 0 WHERE var = 'fingercount'"
			cur.execute(sqlFingerCount)
			con.commit()
			#GPIO.output(17, True) # Tentukan mau ubah relay dari database atau langsung GPIO
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
		exit(1)
	
	## Gets some sensor information
	print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
	
	## Tries to enroll new finger
	try:
		print('Waiting for finger...')
	
		## Wait that finger is read
		while ( f.readImage() == False ):
			pass
	
		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)
	
		## Checks if finger is already enrolled
		result = f.searchTemplate()
		positionNumber = result[0]
	
		if ( positionNumber >= 0 ):
			print('Template already exists at position #' + str(positionNumber))
			exit(0)
	
		print('Remove finger...')
		time.sleep(2)
	
		print('Waiting for same finger again...')
	
		## Wait that finger is read again
		while ( f.readImage() == False ):
			pass
	
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
		exit(1)
	
	#V newfingerflag == 0 ## Update database
	sqlFinger = "UPDATE flag SET flag = 0 WHERE fungsi = 'newfingerflag'"
	cur.execute(sqlFinger)
	con.commit()
#====================================================================#
########## FUNGSI NEW FINGER - END ###################################
######################################################################

######################################################################
### MAIN #############################################################
#====================================================================#
while 1:
	con = MySQLdb.connect("localhost", "root", "", "test")
	cur = con.cursor()

	sqlFlag = "select * from flag where id = '%s'" %(1)
	cur.execute(sqlFlag)
	resultFlag = cur.fetchall()
	for row in resultFlag:
		mode_flag = row[2]

	sqlFlag = "select * from flag where id = '%s'" %(2)
	cur.execute(sqlFlag)
	resultFlag = cur.fetchall()
	for row in resultFlag:
		speed_flag = row[2]
	
	sqlFlag = "select * from flag where id = '%s'" %(3)
	cur.execute(sqlFlag)
	resultFlag = cur.fetchall()
	for row in resultFlag:
		alarm_flag = row[2]
	
	sqlFlag = "select * from flag where id = '%s'" %(4)
	cur.execute(sqlFlag)
	resultFlag = cur.fetchall()
	for row in resultFlag:
		finger_flag = row[2]
	
	sqlFlag = "select * from flag where id = '%s'" %(5)
	cur.execute(sqlFlag)
	resultFlag = cur.fetchall()
	for row in resultFlag:
		newfinger_flag = row[2]
	
	print mode_flag
	print speed_flag
	print alarm_flag
	print finger_flag
	print newfinger_flag
	
	if mode_flag == 1:
		mode()
	elif speed_flag == 1:
		speed()
	elif alarm_flag == 1:
		alarm()
	elif finger_flag == 1:
		finger()
	elif newfinger_flag == 1:
		newfinger()
	else:
		pass
#====================================================================#
### MAIN END #########################################################
######################################################################
	