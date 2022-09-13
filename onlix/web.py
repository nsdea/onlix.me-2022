#!/usr/bin/python3
from flask_qrcode import QRcode
from flask_caching import Cache

from flask_limiter import Limiter
from logging.config import dictConfig
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

import os
import time
import flask
import logging

import tools



log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = flask.Flask(__name__, static_url_path='/')
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 * 1000 # 1 GB
app.config.from_mapping({
    "CACHE_TYPE": "SimpleCache",
    "DEBUG": True,
    "CACHE_DEFAULT_TIMEOUT": 300
})
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

from cdn import cdn_bp
from api import api_bp
from blog import blog_bp
from main import main_bp

app.register_blueprint(cdn_bp)
app.register_blueprint(api_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(main_bp)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=['10000 per day', '600 per hour', '60 per minute', '20 per second']
)

# === FLASK LIBRARIES ===
QRcode(app)
cache = Cache(app)
# === MODULES ===

# tools.yml('data/error-modules', {})
# modules = [f.split('.')[0] for f in os.listdir() if (f.endswith('.py') and f.split('.')[0] not in tools.yml('config/disabled-modules'))]

# for module in modules:
#     try:
#         exec(f'import {module}')
#         exec(f'{module}.register(app, cache)')
#     except Exception as e:
#         print(f'[ERROR] {module}: {e}')
        
#         error_yml = tools.yml('data/error-modules')
#         error_yml[module] = str(e)
#         tools.yml('data/error-modules', error_yml)
#     else:
#         print(f'+ {module}.py')

@limiter.request_filter
def ip_whitelist():
    return tools.ip(flask.request) in tools.yml('config/no-ratelimit-ips')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(levelname)s in %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'WARN',
        'handlers': ['wsgi']
    }
})

def main():
    app.run(port=tools.yml('config/main')['port'], debug=True)
    open('logs/last_restart.txt', 'w').write(str(time.time()))

if __name__ == '__main__':
    main()