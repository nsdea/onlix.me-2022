import os
import flask

from io import BytesIO
from datetime import datetime

import blog
import tools

DEFAULT_MODULES = ['tools', 'web']

main_bp = flask.Blueprint('main_bp',
    __name__,
)

@main_bp.route('/')
def home():        
    return tools.render('home.html')

@main_bp.route('/contact')
def contact():        
    return tools.render('contact.html')

def legal_page() -> str:
    return tools.render('legal.html', last_update=datetime.fromtimestamp(os.path.getmtime(f'templates/legal.html')).strftime('%a %d/%m/%Y %H:%M:%S'))

def legal_page_raw() -> str:
    return '<h3>You are currently viewing the raw version of <a href="/legal">the ONLIX legal document</a>.</h3>\n' + legal_page().split('<!-- START ONLIX LEGAL PAGE -->')[1].split('<!-- END ONLIX LEGAL PAGE -->')[0]
@main_bp.route('/legal')
def legal():        
    return legal_page()

@main_bp.route('/legal/raw')
def legal_raw():
    return legal_page_raw()    

@main_bp.route('/legal/raw/download')
def legal_raw_download():
    return flask.send_file(BytesIO(legal_page_raw().encode('utf-8')), mimetype='text/html', attachment_filename='onlix_legal_raw.html' ,as_attachment=True)
