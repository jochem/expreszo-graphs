from flask import Flask, abort, make_response, render_template
from rrd.graph import rrdgraph

app = Flask(__name__)
graph_types = ('visitors', 'chat', 'members', 'oposts', 'posts', 'topics')


@app.route('/graphs/')
def index():
    return render_template('graphs/index.html')


@app.route('/graphs/<graph_type>/')
def detail(graph_type):
    if not graph_type in graph_types:
        abort(404)
    return render_template('graphs/detail.html', graph_type=graph_type)


@app.route('/graphs/<graph_type>/<start>.png')
@app.route('/graphs/<graph_type>/<int:width>/<start>.png')
def png(graph_type, start=None, width=597):
    if not graph_type in graph_types:
        abort(404)

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
    app.debug = True
    app.run()
