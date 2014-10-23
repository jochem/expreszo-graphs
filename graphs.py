from flask import Flask, abort, make_response, render_template
from rrd.graph import rrdgraph

from settings import DEBUG, graph_types

app = Flask(__name__)


def require_valid_graph(function):
    def wrapper(graph_type):
        if graph_type not in graph_types:
            abort(404)
    return function


@app.route('/graphs/')
@require_valid_graph
def index():
    return render_template('graphs/index.html')


@app.route('/graphs/<graph_type>/')
@require_valid_graph
def detail(graph_type):
    return render_template('graphs/detail.html', graph_type=graph_type)


@app.route('/graphs/<graph_type>/<start>.png')
@app.route('/graphs/<graph_type>/<int:width>/<start>.png')
@require_valid_graph
def png(graph_type, start=None, width=597):
    if width < 107:
        width = 107
    elif width > 2000:
        width = 2000
    width -= 97

    rg = rrdgraph(str(width))
    start = str(start)
    image_data = getattr(rg, graph_type)('-' + start, start)

    response = make_response(image_data)
    response.mimetype = "image/png"
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = DEBUG
    app.run()
