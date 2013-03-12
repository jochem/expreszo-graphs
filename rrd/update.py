#!/usr/bin/env python
#
# Jochem, november 2010

import datetime, re, rrdtool, time
from os import uname
from urllib2 import Request, urlopen
from urllib2 import URLError

""" Settings """
datadir         = '/home/expreszo/expreszo/graphs/data/'
rrd_file        = datadir + 'expreszo.rrd'
forum_url	= 'http://www.expreszo.nl/forum/index.php'

def create():
	rrdtool.create(rrd_file, '--step', '300', '--start', '0',
		'DS:total:GAUGE:600:0:U',
		'DS:registered:GAUGE:600:0:U',
		'DS:hidden:GAUGE:600:0:U',
		'DS:guests:GAUGE:600:0:U',
		'DS:chat:GAUGE:600:0:U',
		'DS:posts:GAUGE:600:0:U',
		'DS:topics:GAUGE:600:0:U',
		'DS:members:GAUGE:600:0:U',
		'RRA:AVERAGE:0.5:1:2017', # every 5 minutes for 1 week
		'RRA:AVERAGE:0.5:4:2161', # every 20 minutes for 1 month
		'RRA:AVERAGE:0.5:12:2161', # every 60 minutes for 3 months
		'RRA:AVERAGE:0.5:144:361', # every 720 minutes (12 hours), 6 months
		'RRA:AVERAGE:0.5:288:366', # every 1440 minutes (24 hours), for 1 year
		'RRA:AVERAGE:0.5:2016:261') # every 10080 minutes (168 hours, 1 week), for 5 years
		# alles +1 extra

def update():
	log("Reading %s" % forum_url)
	req = Request(forum_url)
	req.add_header("User-Agent", "Expreszo Grapher/1.3 (+http://expreszo.djangohost.nl/graphs/)")
	try:
		response = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			log("Couldn't reach the server. Reason: %s" % e.reason)
		elif hasattr(e, 'code'):
			log("The server returned a %s code" % e.code)
	else:
		html = response.read()
		a = re.search(b"Er zijn in totaal <strong>(?P<total>\d+)</strong> gebruikers online :: (?P<registered>\d+) geregistreerde, (?P<hidden>\d+) verborgen en (?P<guests>\d+) gasten", html)
		b = re.search(b"<p>Totaal aantal berichten <strong>(?P<posts>\d+)</strong> &bull; Totaal aantal onderwerpen <strong>(?P<topics>\d+)</strong> &bull; Totaal aantal leden <strong>(?P<members>\d+)</strong>", html)
		c = re.search(b"<p>Nu aan het chatten: <strong>(.+).</strong></p>", html)
		u = a.groupdict()
		p = b.groupdict()
		log(u)
		log(p)
		if c:
			chat = str(len(c.group(1).split(',')))
		else:
			chat = '0'
		log("%s chatters" % chat)
		try:
			rrdtool.update(rrd_file, 'N:' + 
					u['total'] + ':' +
					u['registered'] + ':' +
					u['hidden'] + ':' +
					u['guests'] + ':' +
					chat + ':' +
					p['posts'] + ':' +
					p['topics'] + ':' +
					p['members'])
		except rrdtool.error as e:
			log(e)

def graph():
	rg = rrdgraph('500')
	rg.chat('-1d', '24 uur')
	rg.chat('-1w', '1 week')
	rg.chat('-1m', '1 maand')
	rg.members('-1d', '24 uur')
	rg.posts('-1d', '24 uur')
	rg.topics('-1d', '24 uur')
	rg.visitors('-1d', '24 uur')
	rg.visitors('-1w', '1 week')
	rg.visitors('-1m', '1 maand')

def log(message):
	l = open(datadir + "update.log", "a")
	l.write(datetime.datetime.now().strftime("%b %d %H:%M:%S") + " " + str(message) + "\n")
	l.close()

try:
	open(rrd_file)
except:
	log("The Round Robin Database does not yet exist, so we're going to create it first.")
	try:
		create()
	except rrdtool.error as e:
		log("It didn't work out, because %s. Exiting now!" % e)
		exit(1)
try:
	update()
except:
	log("Updating failed :<")
	exit(1)
