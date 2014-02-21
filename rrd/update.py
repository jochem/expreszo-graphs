#!/usr/bin/env python
import datetime
import re
import rrdtool
from urllib2 import Request, urlopen
from urllib2 import URLError

import db
from settings import RRD_FILE as rrd_file, FORUM_URL as forum_url, datadir


def update():
    log("Reading %s" % forum_url)
    req = Request(forum_url)
    req.add_header("User-Agent", "Expreszo Grapher/1.4 (+http://expreszo.djangohost.nl/graphs/)")
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
        db.create()
    except rrdtool.error as e:
        log("It didn't work out, because %s. Exiting now!" % e)
        exit(1)
try:
    update()
except:
    log("Updating failed :<")
    exit(1)
