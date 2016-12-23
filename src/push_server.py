#! /usr/bin/python

import flask
from flask import Flask
from flask_cors import CORS
from kafka_service import KafkaService

app = Flask(__name__)
CORS(app)

app.kafka_service = KafkaService()


@app.route('/stream/auth')
def stream_auth():
    return stream_events('success_auth_logs')


@app.route('/stream/anon')
def stream_anon():
    return stream_events('success_anon_logs')


@app.route('/stream/err')
def stream_err():
    return stream_events('err_logs')


def stream_events(topic):
    return flask.Response(app.kafka_service.stream_event(topic), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)