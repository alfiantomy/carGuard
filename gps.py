import time
import urllib2, urllib
import gps
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

######################################################################
### FUNGSI GPS - START ##############################################
#====================================================================#
report = session.next()
if hasattr(report, 'lat'):
	print 'latitude:  ' , report.lat
	
if hasattr(report, 'lon'):
	print 'longitude: ' , report.lon	

myUpdate=[('lat', report.lat), ('lon', report.lon)]
myUpdate=urllib.urlencode(myUpdate)
path='http://carguard.000webhostapp.com/gps.php'
req=urllib2.Request(path, myUpdate)
page=urllib2.urlopen(req).read()
print page
#====================================================================#
### FUNGSI GPS - END #################################################
######################################################################