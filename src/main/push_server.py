#! /usr/bin/python

import flask
from flask import Flask
from flask_cors import CORS
from kafka_consumer import KafkaConsumer
import app_util

app = Flask(__name__)
CORS(app)

app.kafka_consumer = None


@app.route('/register')
def register():
    return __create_success_response({
        "subscriber_id": __get_kafka_consumer().register(),
        "success": True
    })


@app.route('/subscribe/<subscriber_id>/<topic>')
def subscribe(subscriber_id, topic):
    return flask.Response(
        __get_kafka_consumer().subscribe(subscriber_id, __get_encoded(topic)),
        mimetype='text/event-stream')


@app.route('/unsubscribe/<subscriber_id>/<topic>')
def unsubscribe(subscriber_id, topic):
    if __get_kafka_consumer().unsubscribe(subscriber_id, topic):
        return __create_success_response({
            "success": True
        })
    else:
        return __create_invalid_client_id_response(subscriber_id)


def __create_success_response(data):
    return flask.jsonify(data)


def __create_invalid_client_id_response(subscriber_id):
    return flask.jsonify({
        "subscriber_id": subscriber_id,
        "success": False,
        "msg": "Invalid subscriber id"
    })


def __get_encoded(topic):
    return topic.encode('ascii')


def __get_kafka_consumer():
    if app.kafka_consumer is None:
        app.kafka_consumer = KafkaConsumer()
    return app.kafka_consumer


if __name__ == '__main__':
    app.kafka_consumer = KafkaConsumer()
    app.run(debug=True,
            threaded=True,
            port=app_util.read_conf('PushServer', 'port', 5000, int))
