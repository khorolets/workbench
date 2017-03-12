#! /usr/bin/env python3
__version__ = '0.2.0'

import os

from flask import (
    Flask,
    jsonify,
    render_template,
    render_template_string,
    Response,
    request,
)

from .core import render, render_dist, default_config

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'))

_possible_answers = ['n', 'Y']


@app.route('/')
def  greeting():
    """
    Default (root) endpoint of the Workbench to provide basic information and initiate
    initial_data_structure() function which creates basic structure
    """
    initial_data_structure(include_config=False)

    greeting_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Workbench Greeting</title>
        <style>
        body {
            max-width: 1170px;
            margin: 0 auto;
            font-family: Helvetica, Arial, sans-serif;
            background-color: #F1F1F1;
        }
        a {
            color: #0080FF;
            text-decoration: underlined;
        }
        a:hover {
            text-decoration: none;
        }
        a:visited {
            color: #800040;
        }
        code {
            padding: 2px 4px;
            font-size: 90%;
            color: #c7254e;
            background-color: #f9f2f4;
            border-radius: 4px
        }
        pre {
            display: block;
            padding: 9.5px;
            margin: 0 0 10px;
            font-size: 13px;
            line-height: 1.42857143;
            color: #333;
            word-break: break-all;
            word-wrap: break-word;
            background-color: #f5f5f5;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        </style>
    </head>
    <body>
    <h1>Welcome to Workbench app!</h1>
    <p>The main purpose of this application is to help markupers (a.k.a. PSD2HTML developers) to save a lot of time with <a href="http://jinja.pocoo.org/docs/2.9/">Jinja2</a> template engine</p>

    <p>Your files:</p>
    <ol>
        {% for f in files %}
            <li><a href="/page/{{ f }}">{{ f }}</a></li>
        {% else %}
            <p>No files found in <code>templates</code> directory yet. </p>
        {% endfor %}
    </ol>
    <p>Your static is server from: <code>{{ static_dir }}</code>

    <h2>Commands:</h2>
    <p>Workbench has tree main commands:</p>
    <ul>
        <li><code>workbench runserver</code> &mdash; starts the application and you can access this greeting page by opening <a href="http://localhost:5000/">http://localhost:5000/</a> in your browser. Press <code>Ctrl + C</code> to stop it.</li>
        <li><code>workbench build</code> &mdash; prepares your markup to distribution. It creates a directory called <code>dist</code> where all your pages will be stored together with the structure of dirs and files from <code>static</code>. Then you can pack <code>dist</code> and send it further to someone who'll be implementing your work. <strong>P.S.</strong> If your team already uses Jinja2 it'd be better to share your <code>static</code> and <code>templates</code> dirs as they are.</li>
        <li><code>workbench initial_data_structure</code> &mdash; creates necessary directories for your workbench project. (Runs automatically without config creation each time you open greeting page)</li>
    </ul>

    <h2>How to work with Elizabeth:</h2>
    <p>Workbench is using <a href="http://elizabeth.readthedocs.io/en/latest/index.html">Elizabeth</a> to give you a way to use different fake data.</p>
    <p>In all templates you're creating <code>elizabeth</code> variable is available for you in two different ways.</p>
    <h3>If <code>config.json</code> is in the root</h3>
    <p>In that case <a href="http://elizabeth.readthedocs.io/en/latest/index.html#usage">Elizabeth's Generic class</a> initiated with the language specified in config and you can use it like that:</p>
    {% raw %}
    <pre><p>{{ elizabeth.personal.full_name('female') }}</p></pre>
    {% endraw %}

    <h3>If there is no <code>config.json</code> in the root</h3>
    <p>In that case <code>elizabeth</code> variable is still available but the way of usage is changing a little bit:</p>
    {% raw %}
    <pre><p>{{ elizabeth.Personal('en').full_name('female') }}</p></pre>
    {% endraw %}
    <p>As you can see you have to initiate Elizabeth's classes manually and pass a language code before you can get a result.</p>

    <h3>The most important information of how to work with Elizabeth</h3>
    <p>First of all you need to know the way your <code>elizabeth</code> is initiated and then you can use it according to the <a href="http://elizabeth.readthedocs.io/en/latest/guide.html">Elizabeth's official guide</a>. </p>

    <h2>Issues</h2>
    <p>If you have any questions or propositions, fill free to create an issue at <a href="https://github.com/khorolets/workbench/issues">GitHub Workbench issues page</a></p>

    </body>
    </html>
    '''
    context = {
        'files': html_files(),
        'static_dir': os.path.join(os.getcwd(), 'static')
    }
    return Response(render_template_string(greeting_template, **context))


@app.route('/page/<string:filename>')
def  page(filename):
    return Response(render(filename, {}))


def build(force=False):
    """
    Prepares the work to distribution
    """
    import shutil
    print("Building...")
    if os.path.exists('./dist'):
        user_answer = 'Y' if force else None
        while user_answer not in _possible_answers:
            user_answer = input("dist is already exist, if you continue it would be replaced with the new one. [Y/n]: ")
            if user_answer == 'y':
                user_answer = input('Did you mean Y (capital letter)? [Y/n]: ')
        if user_answer.lower() == 'n':
            print('Aborting...')
            return

        shutil.rmtree('./dist')
    shutil.copytree('./static', './dist')
    for file_ in html_files():
        with open('./dist/%s' % file_, 'w') as f:
            f.write(render_dist(file_, {}))
    print("Done.")


def initial_data_structure(include_config=True):
    """
    Creates initial data structure for your Workbench project in the current directory
    """
    if not os.path.exists('./config.json') and include_config:
        with open('./config.json', 'w') as f:
            f.write(default_config(dump=True))
    if not os.path.exists('./templates'):
        os.makedirs('./templates')
    if not os.path.exists('./static'):
        os.makedirs('./static')


def html_files():
    for file_ in os.listdir('./templates'):
        if os.path.join('./templates', file_) and not file_.startswith('_'):
            yield file_
