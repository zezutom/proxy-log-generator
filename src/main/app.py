#! /usr/bin/python

from flask import Flask, render_template

import app_util

app = Flask(__name__)
app.template_folder = app_util.get_template_folder()
app.static_folder = app_util.get_static_folder()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=app_util.read_conf('App', 'port', 3000, int))
