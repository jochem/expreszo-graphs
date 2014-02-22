import os

DEBUG = False

datadir = './data/'
graph_types = ('visitors', 'chat', 'members', 'posts', 'topics')

RRD_FILE = os.path.join(datadir, 'expreszo.rrd')
FORUM_URL = 'http://www.expreszo.nl/forum/index.php'
