'''
Created on Sep 22, 2017

@author: Tomy
'''

#import RPi.GPIO as GPIO
import MySQLdb

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
	
	if mode_counter == 1:
		pass
		#V Ubah fingercount == 1
		sqlFingerCount = "UPDATE flag SET counter = 1 WHERE var = 'fingercount'"
		cur.execute(sqlFingerCount)
		con.commit()
		# Ubah relay_finger == 0
		
	elif mode_counter == 0:
		pass
		#V Ubah fingercount == 0
		sqlFingerCount = "UPDATE flag SET counter = 0 WHERE var = 'fingercount'"
		cur.execute(sqlFingerCount)
		con.commit()
		# Ubah relay_finger == 1
        
	#V modeflag == 0 ## Update database
	sqlMode = "UPDATE flag SET flag = 0 WHERE fungsi = 'modeflag'"
	cur.execute(sqlMode)
	con.commit()

	
def speed():
	con = MySQLdb.connect("localhost", "root", "admin", "tes")
	cur = con.cursor()
	sqlSpeed = "select * from counter where var = '%s'" %("speedcount")
	cur.execute(sqlSpeed)
	resultSpeed = cur.fetchall()

	for row in resultSpeed:
		index = row[0]
		fspeedcount = row[1]
		speed_counter = row[2]
    
	if speed_counter == 1:
		mekanik_speed == 1 # Ayo ndang dibuat
	elif speed_counter == 0:
		mekanik_speed == 0 # Ayo ndang dibuat
        
	#V speedflag == 0 ## Update database
	sqlSpeed = "UPDATE flag SET flag = 0 WHERE fungsi = 'speedflag'"
	cur.execute(sqlSpeed)
	con.commit()
    

def alarm():
	con = MySQLdb.connect("localhost", "root", "admin", "tes")
	cur = con.cursor()
	sqlAlarm = "select * from counter where var = '%s'" %("alarmcount")
	cur.execute(sqlAlarm)
	resultAlarm = cur.fetchall()

	for row in resultAlarm:
		index = row[0]
		falarmcount = row[1]
		alarm_counter = row[2]
    
	if alarm_counter == 1:
		relay_alarm == 1
	elif alarm_counter == 0:
		relay_alarm == 0
        
	#V alarmflag == 0 ## Update database
	sqlAlarm = "UPDATE flag SET flag = 0 WHERE fungsi = 'alarmflag'"
	cur.execute(sqlAlarm)
	con.commit()


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
		relay_finger == 0
	elif finger_counter == 0:
		relay_finger == 1
    
	#V fingerflag == 0 ## Update database
	sqlFinger = "UPDATE flag SET flag = 0 WHERE fungsi = 'fingerflag'"
	cur.execute(sqlFinger)
	con.commit()
	


#############################################################
### MAIN ####################################################
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
		safefinger_flag = row[2]
	
	print mode_flag
	print speed_flag
	print alarm_flag
	print finger_flag
	print safefinger_flag
	
	if mode_flag == 1:
		mode()
	elif speed_flag == 1:
		speed()
	elif alarm_flag == 1:
		alarm()
	elif finger_flag == 1:
		finger()
	elif safefinger_flag == 1:
		savefinger()
	else:
		pass

	