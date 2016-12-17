#! /usr/bin/python

import json
from time import sleep

import flask
from flask import Flask, render_template
from kafka import KafkaConsumer

app = Flask(__name__)

consumer = KafkaConsumer('all_logs')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def categorise_logs():
    return flask.Response(stream_logs(), mimetype="text/event-stream")


def stream_logs():
    for msg in consumer:
        log = json.loads(msg.value)
        user = log.get('authenticated', '-')

        event = {
            'success': True if log.get('res_status') == 200 else False,
            'user': user,
            'anonymous': True if user == '-' else False,
            'url': log.get('url')
        }
        sleep(0.5)
        yield "data: {}\n\n".format(json.dumps(event))


if __name__ == '__main__':
    app.run(debug=True)