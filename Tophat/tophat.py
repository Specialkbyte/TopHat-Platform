#!/usr/bin/env python2.7

from twisted.internet import reactor, ssl
from os import getuid, setuid, setgid
from pwd import getpwnam
from grp import getgrnam
from sys import exit,path
from twisted.internet.error import CannotListenError
#Import the controllers.
from Controllers.TopHatProtocol import *
from Common.Miscellaneous import printTopHat
def TophatMain():
	printTopHat()
	if getuid() is not 0:
		print "The TopHat-service must be started as root to bind to port 443"
		print "[TopHat-Serivce failed to start]"
		exit(1)
	
	factory = TopHatFactory() 
	try:
		reactor.listenSSL(443, factory, ssl.DefaultOpenSSLContextFactory('/etc/ssl/private/tophat.key', '/etc/ssl/certs/tophat.crt'), interface='0.0.0.0')
	except CannotListenError:
		print "The port 443 is already bound, please kill the process using that before launching the Tophat-Service."
		print "[TopHat-Serivce failed to start]"
		exit(1)

	print "Listening on port 443, deadly."


	try:
		uidNumber= getpwnam('tophat')[2]
		print "Dropped privileges to user 'tophat'. Cool pops."
	except KeyError:
		print "Failed to drop privileges to user 'tophat'. Uh-oh."
		print "Attempting to drop to user 'nobody'"
		try:
			uidNumber= getpwnam('nobody')[2]
			print "Dropped privileges to 'nobody'. Phew!"
		except:
			print "No user 'nobody' on this system, bit mad, I'm outta here so."
			print "[TopHat-Service failed to start]"
			exit(1)
	try:
		gidNumber= getgrnam('tophat')[2]
		print "Dropped privileges to group 'tophat'. Nice."
	except KeyError:
		print "Failed to drop privileges to group 'tophat'. :-S"
		print "Attempting to drop to group 'daemon'"
		try:
			gidNumber= getgrnam('daemon')[2]
			j
			print "Dropped privileges to group 'daemon'. It seems we're in the clear, for now."
		except:
			print "No group 'nobody' on this system, I'm not going to let you run me as root. Sorry."
			print "[TopHat-Serivce failed to start]"
			exit(1)

	setgid(uidNumber)
	setuid(gidNumber)
	print "[TopHat-Service started successfully]"
	try:
		reactor.run()
	except KeyError:
		reactor.stop()
		print "[TopHat-Service shutting down]"
		exit(0)

if __name__ == '__main__':
	TophatMain()
