'''
Created on Sep 22, 2017

@author: Tomy
'''

##import RPi.GPIO as GPIO
import MySQLdb
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import time

######################################################################
### FUNGSI MAIN - START ##############################################
#====================================================================#
def main():
	while 1:
		con = MySQLdb.connect("localhost", "root", "admin", "test")
		cur = con.cursor()
		

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
			#GPIO.output(17, True)
			pass
		elif relay_finger == 0:
			#GPIO.output(17, False)
			pass
		if relay_alarm == 1:
			#GPIO.output(18, True)
			pass
		elif relay_alarm == 0:
			#GPIO.output(18, False)
			pass
		## RELAY END
		
		## FLAG START
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
			
		sqlFlag = "select * from flag where id = '%s'" %(6)
		cur.execute(sqlFlag)
		resultFlag = cur.fetchall()
		for row in resultFlag:
			delfinger_flag = row[2]
		
		print mode_flag
		print speed_flag
		print alarm_flag
		print finger_flag
		print newfinger_flag
		print delfinger_flag
		print('==========')
		
		if mode_flag == 1:
			mode()
		elif speed_flag == 1:
			speed()
		elif alarm_flag == 1:
			alarm()
		elif finger_flag == 1:
			finger()
		elif newfinger_flag == 1:
			new_finger()
		elif delfinger_flag == 1:
			del_finger()
		else:
			pass
		## FLAG END
#====================================================================#
### FUNGSI MAIN END ##################################################
######################################################################


######################################################################
########## FUNGSI MODE - START #######################################
#====================================================================#
def mode():
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()
	sqlMode = "select * from counter where var = '%s'" %("modecount")
	cur.execute(sqlMode)
	resultMode = cur.fetchall()

	for row in resultMode:
		mode_counter = row[2]

	if mode_counter == 1:
		#V Ubah fingercount = 1
		sqlFingerCount = "UPDATE counter SET counter = 1 WHERE var = 'fingercount'"
		cur.execute(sqlFingerCount)
		con.commit()
		finger()

	elif mode_counter == 0:
		#V Ubah fingercount = 0
		sqlFingerCount = "UPDATE counter SET counter = 0 WHERE var = 'fingercount'"
		cur.execute(sqlFingerCount)
		con.commit()
		sqlRelayFinger = "UPDATE relay SET status = 0 WHERE  relay = 'relay_finger'"
		cur.execute(sqlRelayFinger)
		con.commit()
		
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
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()
	sqlSpeed = "select * from counter where var = '%s'" %("speedcount")
	cur.execute(sqlSpeed)
	resultSpeed = cur.fetchall()

	for row in resultSpeed:
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
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()
	sqlAlarm = "select * from counter where var = '%s'" %("alarmcount")
	cur.execute(sqlAlarm)
	resultAlarm = cur.fetchall()

	for row in resultAlarm:
		alarm_counter = row[2]
	
	if alarm_counter == 1:
		sqlRelayAlarm = "UPDATE relay SET status = 1 WHERE  relay = 'relay_alarm'"
		cur.execute(sqlRelayAlarm)
		con.commit()
	elif alarm_counter == 0:
		sqlRelayAlarm = "UPDATE relay SET status = 0 WHERE  relay = 'relay_alarm'"
		cur.execute(sqlRelayAlarm)
		con.commit()
		
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
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()
	sqlFinger = "select * from counter where var = '%s'" %("fingercount")
	cur.execute(sqlFinger)
	resultFinger = cur.fetchall()

	for row in resultFinger:
		finger_counter = row[2]
	
	if finger_counter == 1:
		sqlRelayFinger = "UPDATE relay SET status = 1 WHERE  relay = 'relay_finger'"
		cur.execute(sqlRelayFinger)
		con.commit()
		need_finger()
	elif finger_counter == 0:
		sqlRelayFinger = "UPDATE relay SET status = 0 WHERE  relay = 'relay_finger'"
		cur.execute(sqlRelayFinger)
		con.commit()
		sqlModeCount = "UPDATE counter SET counter = 0 WHERE var = 'modecount'"
		cur.execute(sqlModeCount)
		con.commit()
	
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
			con = MySQLdb.connect("localhost", "root", "admin", "test")
			cur = con.cursor()			
			sqlFinger = "select * from counter where var = '%s'" %("fingercount")
			cur.execute(sqlFinger)
			resultFinger = cur.fetchall()
	
			for row in resultFinger:
				finger_counter = row[2]
		
			if finger_counter == 0:
				sqlRelayFinger = "UPDATE relay SET status = 0 WHERE  relay = 'relay_finger'"
				cur.execute(sqlRelayFinger)
				con.commit()
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
			con = MySQLdb.connect("localhost", "root", "admin", "test")
			cur = con.cursor()			
			sqlFingerCount = "UPDATE counter SET counter = 0 WHERE var = 'fingercount'"
			cur.execute(sqlFingerCount)
			con.commit()
			finger()
#====================================================================#
########## FUNGSI SCAN FINGER - END ##################################
######################################################################


######################################################################
########## FUNGSI NEW FINGER - START #################################
#====================================================================#
def new_finger():
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()	
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
			con = MySQLdb.connect("localhost", "root", "admin", "test")
			cur = con.cursor()			
			sqlNewFinger = "select * from flag where fungsi = '%s'" %("newfingerflag")
			cur.execute(sqlNewFinger)
			resultNewFinger = cur.fetchall()
	
			for row in resultNewFinger:
				new_finger_flag = row[2]
		
			if new_finger_flag == 0:
				main()
	
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
			con = MySQLdb.connect("localhost", "root", "admin", "test")
			cur = con.cursor()			
			sqlNewFinger = "select * from flag where fungsi = '%s'" %("newfingerflag")
			cur.execute(sqlNewFinger)
			resultNewFinger = cur.fetchall()
	
			for row in resultNewFinger:
				new_finger_flag = row[2]
		
			if new_finger_flag == 0:
				main()
	
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

	finger_info()
	#V newfingerflag == 0 ## Update database
	sqlFinger = "UPDATE flag SET flag = 0 WHERE fungsi = 'newfingerflag'"
	cur.execute(sqlFinger)
	con.commit()
	main()
#====================================================================#
########## FUNGSI NEW FINGER - END ###################################
######################################################################


######################################################################
########## FUNGSI NEW FINGER - START #################################
#====================================================================#
def del_finger():
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()	
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
	
		con = MySQLdb.connect("localhost", "root", "admin", "test")
		cur = con.cursor()			
		sqlDelFinger = "select * from finger_del where id = '1'"
		cur.execute(sqlDelFinger)
		resultDelFinger = cur.fetchall()	
		for row in resultDelFinger:
			del_finger_template = row[2]	
		
		positionNumber = del_finger_template
		
		if ( f.deleteTemplate(positionNumber) == True ):
			print('Template deleted!')

	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		exit(1)

	finger_info()
	#V delfingerflag == 0 ## Update database
	sqlFinger = "UPDATE flag SET flag = 0 WHERE fungsi = 'delfingerflag'"
	cur.execute(sqlFinger)
	con.commit()
	main()
#====================================================================#
########## FUNGSI NEW FINGER - END ###################################
######################################################################


######################################################################
########## FUNGSI FINGER INFO - START ##################################
#====================================================================#
def finger_info():
	con = MySQLdb.connect("localhost", "root", "admin", "test")
	cur = con.cursor()	

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
	#print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
	used = int(f.getTemplateCount())
	sqlFinger = "UPDATE finger_info SET value = %d WHERE parameter = 'used'" %(used)
	cur.execute(sqlFinger)
	con.commit()
	
	tableIndex = f.getTemplateIndex(0)
	for i in range(0, 4):
		#print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))
		index = str(tableIndex[i])
		sqlFinger = "UPDATE finger_info SET value = %s WHERE id = '%d'" %(index,i+2)
		cur.execute(sqlFinger)
		con.commit()
#====================================================================#
### FUNGSI FINGER INFO - END #########################################
######################################################################



######################################################################
########## START #####################################################
#====================================================================#
main()
#====================================================================#
########## END #######################################################
######################################################################
	

