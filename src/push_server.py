#! /usr/bin/python

import flask
from flask import Flask
from flask_cors import CORS
from kafka_service import KafkaService

app = Flask(__name__)
CORS(app)

app.kafka_service = KafkaService()


@app.route('/stream')
def stream_logs():
    return stream_events('proxy_logs')


def stream_events(topic):
    return flask.Response(app.kafka_service.stream_event(topic), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True)
