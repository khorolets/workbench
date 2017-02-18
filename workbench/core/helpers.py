"""
Helper functions
"""
import elizabeth
import jinja2
import json
import os

from flask import url_for


def static(path):
    """
    Wraps flask's `url_for` function to simplify the usage
    """
    return url_for('static', filename=path)


def init_elizabeth():
    if not os.path.exists('./config.json'):
        return elizabeth
    with open('./config.json', 'r') as f:
        config = json.loads(f.read())
    return elizabeth.Generic(config['elizabeth_language'])


def init_jinja2():
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('./templates/'),
        )
    env.globals.update({
            'static': static,
            'elizabeth': init_elizabeth()
            # 'url': reverse,
        })
    return env

def render(filename, context):
    """
    Helper function to render Jinja2 template from file without realoading the app
    Args:
        filename<str>: name of template file
        context<dict>: context dict
    """
    env = init_jinja2()
    return env.get_template(filename).render(context)


def render_dist(filename, context):
    env = init_jinja2()
    env.globals.update({
            'static': lambda path: path,
        })
    return env.get_template(filename).render(context)


def default_config(dump=False):
    """
    Returns default config for the app

    Args:
        dump <bool>: flag to permit json.dumps before return

    Returns config dict or config json string relying on the `dump` flag
    """
    config = {
        'elizabeth_language': 'en',
    }
    if dump:
        config = json.dumps(config)
    return config
