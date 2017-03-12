# Workbench README

The main purpose of this app is to save time for markupers (a.k.a. PSD2HTML) by providing them a tool where they can easily use [Jinja2](https://github.com/pallets/jinja) template engine.

*Workbench* is built over the [Flask](https://github.com/pallets/flask) (Python microframework) and works only with **Python 3**.

## What does it do?
You can simply use the advantages of *extending* and *including* templates, *loops* and, probably, other good stuff from **Jinja2**.

When your work is done you simple build your templates in a separate directory by one command and then just pack and share it.

## Available commands
* `workbench version` - returns version of package.
* `workbench runserver` - runs *Flask* server
* `workbench build` - renders all the templates from `templates` into separate html files and places them in `dist` directory together with the `static` directory content (saving its structure)
* `workbench initial_data_structure` - creates necessary directory structure in the current directory (`static`, `templates` and `config.json` will be created). This command runs when you visit http://localhost:5000/ except the `config.json`

## Installation
**Important note:** I'm going to create PyPi package in near future to simplify the installation to `pip install Workbench` or something similar. So this may change soon.

```bash
$ pip install git+https://github.com/khorolets/workbench.git@master
```

~Note that may be you'll need to use `pip3` if you have different versions of Python.~


## Quick guide

```bash
$ mkdir my_project && cd my_project
$ workbench runserver
```

or if you prefer Docker:

```bash
$ mkdir my_project && cd my_project
$ docker run --rm -it -v $(pwd):/www -p 5000:5000 khorolets/workbench runserver
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

**Flask** server will be started and you can open http://localhost:5000/ to see the greeting page.

After the visiting of the greeting page in your `my_project` root two directories would be created: `static` and `templates`

Create `templates/_base.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sitetitle</title>
    <link rel="stylesheet" type="text/css" href="{{ static('css/style.css') }}">
</head>
<body>
{% block main %}{% endblock %}
</body>
</html>
```

Create `templates/index.html`:

```html
{% extends "_base.html" %}
{% block main %}
    <h1>Hello world</h1>
{% endblock %}
```

Open http://localhost:5000/page/index.html to see your "Hello world". If you are not familiar with *Jinja2* syntax you can visit the [official template designer documentation](http://jinja.pocoo.org/docs/2.9/templates/)

## Fake data
*Workbench* depends on the great library for generating fake data - [Elizabeth](https://github.com/lk-geimfari/elizabeth) by [@lk-geimfari](https://github.com/lk-geimfari).

It is available for you on every page in `elizabeth` variable.

Common usage example:

```html
{% extends "_base.html" %}
{% block main %}
    <h1>Hello {{ elizabeth.Personal('en').name('male') }}</h1>
{% endblock %}
```

Please, see the [Elizabeth's official documentation](http://elizabeth.readthedocs.io/en/latest/index.html) to learn more about [available providers](http://elizabeth.readthedocs.io/en/latest/guide.html).

## How to work with Elizabeth:
In all templates you're creating `elizabeth` variable is available for you in two different ways.

#### If `config.json` is in the root
In that case [Elizabeth's Generic class](http://elizabeth.readthedocs.io/en/latest/index.html#usage) initiated with the language specified in config and you can use it like that:

    {{ elizabeth.personal.full_name('female') }}

#### If there is no `config.json` in the root</h3>
In that case `elizabeth` variable is still available but the way of usage is changing a little bit:

    {{ elizabeth.Personal('en').full_name('female') }}

As you can see you have to initiate Elizabeth's classes manually and pass a language code before you can get a result.

#### The most important information of how to work with Elizabeth

First of all you need to know the way your `elizabeth` is initiated and then you can use it according to the [Elizabeth's official guide](http://elizabeth.readthedocs.io/en/latest/guide.html). </p>

## Building your work
When your work is finished and you want to build it you need to run `workbench build`

All your files from `templates` directory will be rendered in separate files and placed to `dist` directory.

**Important note:** All the files which filename is starting from `_` will be skipped, so use it for technical parts such as base template, header, footer and other partials.

In the end you'll get the whole bunch of your files near the content of the `static` root in the `dist`.

For example, if you have structure:

```
static/
-- css/
-- -- style.css
-- js/
-- -- scripts.js
-- img/
-- -- logo.png
templates/
-- _base.html
-- _header.html
-- _footer.html
-- _news_record.html
-- index.html
-- page.html
-- news.html
```

The build result will be:

```
css/
-- style.css
js/
-- scripts.js
img/
-- logo.png
index.html
page.html
news.html
```

## Questions and propositions
If you have questions or you have something to propose fill free to create an issue

