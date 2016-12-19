#! /usr/bin/python

import json
from time import sleep

import flask
from flask import Flask
from flask_cors import CORS, cross_origin
from kafka import KafkaConsumer

app = Flask(__name__)
CORS(app)


@app.route('/stream/auth')
def stream_auth():
    return flask.Response(stream_events(KafkaConsumer('success_auth_logs')), mimetype="text/event-stream")


@app.route('/stream/anon')
def stream_anon():
    return flask.Response(stream_events(KafkaConsumer('success_anon_logs')), mimetype="text/event-stream")


@app.route('/stream/err')
def stream_err():
    return flask.Response(stream_events(KafkaConsumer('err_logs')), mimetype="text/event-stream")


def stream_events(consumer):
    for msg in consumer:
        # Wait to give a client a chance to react
        sleep(1)

        # Stream the new message
        yield "data: {}\n\n".format(msg.value)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)