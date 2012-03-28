#!/usr/bin/env python2.7



from twisted.web import server, resource
from twisted.internet import reactor, ssl
from twisted.web.resource import Resource
from twisted.web.server import Site

from os import getuid, setuid, setgid
from pwd import getpwnam
from grp import getgrnam
from sys import exit,path
from twisted.internet.error import CannotListenError
#This is done to allow importing of modules in the upper directory that aren't currently in the PATH
#It works ;_;
path.append('..')

#Import the controllers.
from Controllers.rootrequests import RootRequests
from Controllers.userrequests import UserRequests
from Controllers.gamerequests import GameRequests
from Controllers.TopHatProtocol import *
from Common.Miscellaneous import printTopHat
def main():
	printTopHat()
	if getuid() is not 0:
		print "The TopHat-service must be started as root to bind to port 443"
		print "[TopHat-Serivce failed to start]"
		exit(1)

	printroot = RootRequests()
	root = Resource()

	# Set the basic URLs we have
	#root.putChild("", RootRequests())
	#root.putChild("user", UserRequests())
	#root.putChild("game", GameRequests())
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
			print "Dropped privileges to group 'daemon'. It seems we're in the clear, for now."
		except:
			print "No group 'nobody' on this system, I'm not going to let you run me as root. Sorry."
			print "[TopHat-Serivce failed to start]"
			exit(1)

	setgid(uidNumber)
	setuid(gidNumber)
	print "[TopHat-Service started successfully]"
	reactor.run()

if __name__ == '__main__':
	main()