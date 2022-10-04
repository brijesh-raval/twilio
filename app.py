from urllib import response
from flask import Flask, redirect, render_template,request
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
import base64
import random
# from msilib.schema import Binary
import re
from base64 import b64encode
from xml.sax.saxutils import escape as xml_escape

app = Flask(__name__)


DEFAULT_FONTS = [
    'HelveticaNeue-Light',
    'Helvetica Neue Light',
    'Helvetica Neue',
    'Helvetica',
    'Arial',
    'Lucida Grande',
    'sans-serif',
]

DEFAULT_SETTINGS = {
    'width': '200',
    'height': '200',
    'radius': '0',
    'font-family': ','.join(DEFAULT_FONTS),
    'font-size': '80',
    'font-weight': '400',
}

SVG_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" pointer-events="none"
    width="{width}" height="{height}">
    <rect width="{width}" height="{height}" rx="{radius}" ry="{radius}" style="{style}"></rect>
    <text text-anchor="middle" y="50%" x="50%" dy="0.35em"
        pointer-events="auto" fill="#ffffff" font-family="{font-family}"
        style="{text-style}">{text}</text>
</svg>
""".strip()
SVG_TEMPLATE = re.sub('(\s+|\n)', ' ', SVG_TEMPLATE)


DEFAULT_COLORS = [
    "#1abc9c", "#16a085", "#f1c40f", "#f39c12", "#2ecc71", "#27ae60",
    "#e67e22", "#d35400", "#3498db", "#2980b9", "#e74c3c", "#c0392b",
    "#9b59b6", "#8e44ad", "#bdc3c7", "#34495e", "#2c3e50", "#95a5a6",
    "#7f8c8d", "#ec87bf", "#d870ad", "#f69785", "#9ba37e", "#b49255",
    "#b49255", "#a94136",
]


def _from_dict_to_style(style_dict):
    return '; '.join(['{}: {}'.format(k, v) for k, v in style_dict.items()])


def _get_color(text, colors=None):
    if not colors:
        colors = DEFAULT_COLORS
    color_index = random.randint(0, 25)
    # color_index = sum(map(ord, text)) % len(colors)
    # print(color_index)
    return colors[color_index]

def get_svg_avatar(text, **kwargs):

    initials = '=)'

    text = text.strip()
    if text:
        split_text = text.split(' ')
        if len(split_text) > 1:
            initials = split_text[0][0] + split_text[-1][0]
        elif len(split_text) == 1:
            initials = split_text[0][0] + split_text[0][1]

    opts = DEFAULT_SETTINGS.copy()
    opts.update(kwargs)

    style = {
        'fill': _get_color(text, opts.get('colors')),
    }

    text_style = {
        'font-weight': opts.get('font-weight'),
        'font-size': opts.get('font-size') + 'px',
    }

    return SVG_TEMPLATE.format(**{
        'height': opts.get('height'),
        'width': opts.get('width'),
        'radius': opts.get('radius'),
        'style': _from_dict_to_style(style),
        'font-family': opts.get('font-family'),
        'text-style': _from_dict_to_style(text_style),
        'text': xml_escape(initials.upper()),
    }).replace('\n', '')

def get_avatar_data_url(text, **kwargs):
    svg_avatar = get_svg_avatar(text, **kwargs)
    b64_avatar = b64encode(svg_avatar.encode())
    return 'data:image/svg+xml;base64,' + b64_avatar.decode()


@app.route('/avtar/<name>', methods=['GET','POST'])
def avtar(name):
    name_ = name
    response = get_svg_avatar(name_)
    print(get_avatar_data_url(name_))
    return response


if __name__ == "__main__":
    app.run(debug=True)


