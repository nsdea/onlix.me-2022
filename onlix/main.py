import os
import time
import flask
import tools

from io import BytesIO
from datetime import datetime

DEFAULT_MODULES = ['tools', 'web']

main_bp = flask.Blueprint('main_bp',
    __name__,
)

@main_bp.route('/')
def home():        
    """Home page"""
    return tools.render('home.html')

@main_bp.route('/contact')
def contact():        
    """Contact page"""
    return tools.render('contact.html')

def legal_page() -> str:
    """Renders the HTML for the legal page"""
    return tools.render('legal.html', last_update=datetime.fromtimestamp(os.path.getmtime(f'templates/legal.html')).strftime('%a %d/%m/%Y %H:%M:%S'))

def legal_page_raw() -> str:
    """Renders raw content of the legal page, without style etc."""
    return '<h3>You are currently viewing the raw version of <a href="/legal">the ONLIX legal document</a>.</h3>\n' + legal_page().split('<!-- START ONLIX LEGAL PAGE -->')[1].split('<!-- END ONLIX LEGAL PAGE -->')[0]

@main_bp.route('/legal')
def legal():        
    """Actual legal page"""
    return legal_page()

@main_bp.route('/legal/raw')
def legal_raw():
    """Actual raw legal page"""
    return legal_page_raw()    

@main_bp.route('/legal/raw/download')
def legal_raw_download():
    """Downloads the raw legal page"""
    return flask.send_file(BytesIO(legal_page_raw().encode('utf-8')), mimetype='text/html', attachment_filename='onlix_legal_raw.html' ,as_attachment=True)

@main_bp.route('/donate')
def donate():
    """Donation page"""

    donations = tools.yml('data/donations') or {}
    
    if not flask.request.args.get('token'):
        token = tools.generate_token()
        donations[token] = time.time()
        tools.yml('data/donations', edit_to=donations)

        return tools.render('donate.html', token=token)

    return tools.render('donation.html')
