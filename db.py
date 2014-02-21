import rrdtool

from settings import RRD_FILE as rrd_file


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
                   'RRA:AVERAGE:0.5:1:2017',  # every 5 minutes for 1 week
                   'RRA:AVERAGE:0.5:4:2161',  # every 20 minutes for 1 month
                   'RRA:AVERAGE:0.5:12:2161',  # every 60 minutes for 3 months
                   'RRA:AVERAGE:0.5:144:361',  # every 720 minutes (12 hours), 6 months
                   'RRA:AVERAGE:0.5:288:366',  # every 1440 minutes (24 hours), for 1 year
                   'RRA:AVERAGE:0.5:2016:261')  # every 10080 minutes (168 hours, 1 week), for 5 years
                   # alles +1 extra
                   