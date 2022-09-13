import yaml
import flask
import qrcode
import base64

from io import BytesIO
from datetime import datetime

def fix_formatting(text: str):
    return text.replace('  ', '&nbsp;').replace('\n', '\n<br>\n')

def readable_size(size: float):
    return round(size/1000000000, 1)

def ip(request): # PRIVACY NOTICE
    if not request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['REMOTE_ADDR']
    return request.environ['HTTP_X_FORWARDED_FOR']

def yml(path: str, edit_to=None):
    path = f'{path}.yml'

    if not edit_to:
        try:
            with open(path) as f:
                return yaml.load(f.read(), Loader=yaml.SafeLoader)
        except:
            open(path, 'w').write('{}')
            return {}

    with open(path, 'w') as f:
        yaml.dump(edit_to, f, sort_keys=False, default_flow_style=False, indent=4)

def unix_to_readable(unix):
    return datetime.utcfromtimestamp(float(unix)).strftime('%Y/%m/%d %H:%M')

def generate_qr(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img_buf = BytesIO()
    qr.make_image().save(img_buf)
    img_buf.seek(0)

    img_data = img_buf.read()
    img_data = base64.b64encode(img_data)
    img_data = img_data.decode()

    return f'data:image/png;base64,{img_data}'

def render(template: str, notice='', **kwargs):
    return flask.render_template(template, **kwargs).replace("""            <br>
            <i id="render-notice"></i>
""", notice)
