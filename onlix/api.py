import blog
import tools

import flask
import markupsafe

api_bp = flask.Blueprint('api_bp',
    __name__,
    # template_folder='../'
)


@api_bp.route('/ip')
# @cache.cached(timeout=50)
def server_ip():
    return '173.212.213.133'

@api_bp.route('/lila.css')
# @cache.cached(timeout=50)
def lila_css():
    with open('static/styles/lila.css') as f:
        css_data = f.read()
    response = flask.make_response(css_data, 200)
    response.mimetype = "text/css"
    return response

@api_bp.route('/api/post')
def api_text():
    return markupsafe.escape(flask.request.args.get('text'))

@api_bp.route('/api/qr/<data>')
def api_useless(data):
    if flask.request.args.get('show') == 'true': 
        return f'<img src="{tools.generate_qr(data)}">'
    return tools.generate_qr(data)

@api_bp.route('/api/blog')
def api_blog():
    return flask.jsonify(blog.get_posts(with_code=False))

@api_bp.route('/api/blog/<post>')
def api_blog_post(post):
    try:
        return blog.get_info(post)
    except FileNotFoundError:
        return flask.abort(404)

@api_bp.route('/api/login-demo', methods=['POST'])
def login_demo():
    return {
        'form': flask.request.form,
        'data': flask.request.data,
        'json': flask.request.get_json()
    }
