import graphs as flask
import os
import unittest

import db
from settings import datadir


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        flask.app.config['TESTING'] = True
        self.app = flask.app.test_client()
        png_dir = os.path.join(datadir, 'png')
        if not os.path.isdir(png_dir):
            os.makedirs(png_dir)
        open(os.path.join(datadir, 'update.log'), 'a')
        db.create()

    def test_index(self):
        rv = self.app.get('/graphs/')
        assert '<h3>index</h3>' in rv.data

    def test_detail(self):
        rv = self.app.get('/graphs/visitors/')
        assert '<h3>visitors</h3>' in rv.data
        rv = self.app.get('/graphs/nonexistent/')
        assert '404' in rv.data

    def test_png(self):
        rv = self.app.get('/graphs/visitors/1d.png')
        assert rv.content_type == 'image/png'
        rv = self.app.get('/graphs/nonexistent/1d.png')
        assert '404' in rv.data

        rv = self.app.get('/graphs/visitors/100/1d.png')
        assert rv.content_type == 'image/png'
        rv = self.app.get('/graphs/visitors/3000/1d.png')
        assert rv.content_type == 'image/png'

        rv = self.app.get('/graphs/chat/1d.png')
        assert rv.content_type == 'image/png'
        rv = self.app.get('/graphs/members/1d.png')
        assert rv.content_type == 'image/png'
        rv = self.app.get('/graphs/posts/1d.png')
        assert rv.content_type == 'image/png'
        rv = self.app.get('/graphs/topics/1d.png')
        assert rv.content_type == 'image/png'

    def test_404(self):
        rv = self.app.get('/')
        assert '<h1>404</h1>' in rv.data

if __name__ == '__main__':
    unittest.main()
