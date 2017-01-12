#! /usr/bin/python

import uuid
from time import sleep

import flask
from flask import Flask
from flask_cors import CORS
from pykafka import KafkaClient

import app_util

app = Flask(__name__)
CORS(app)

# Client subscriptions to Kafka topics: client_id -> [ topic1, topic2, .. , topicN ]
app.subscriptions = {}


@app.route('/register')
def register_client():
    # generate a random UUID
    client_id = str(uuid.uuid4())
    print 'New client id: "{0}"'.format(client_id)

    # initialise client's subscriptions
    app.subscriptions[client_id] = []

    return create_success_response({
        "client_id": client_id,
        "success": True
    })


@app.route('/subscribe/<client_id>/<topic>')
def subscribe(client_id, topic):
    encoded_topic = get_encoded(topic)
    client = get_kafka_client()

    print 'subscriptions upon subscribe: {0}'.format(app.subscriptions)
    if client_id not in app.subscriptions:
        print 'Invalid client id: "{0}"'.format(client_id)
        return create_invalid_client_id_response(client_id)

    # Maintain a list of the client's subscriptions
    client_subscriptions = app.subscriptions[client_id]
    client_subscriptions.append(encoded_topic)

    def consume_events():
        for e in client.topics[encoded_topic].get_simple_consumer():
            if encoded_topic not in app.subscriptions[client_id]:
                print 'Exiting the channel, subscription to \'{0}\' has been cancelled'.format(encoded_topic)
                break

            sleep(1)    # give the subscribed client a chance to react
            yield 'data: {0}\n\n'.format(e.value)

    return flask.Response(consume_events(), mimetype="text/event-stream")


@app.route('/cancel/<client_id>/<topic>')
def cancel_subscription(client_id, topic):

    if client_id not in app.subscriptions:
        print 'Invalid client id: "{0}"'.format(client_id)
        return create_invalid_client_id_response(client_id)

    client_subscriptions = app.subscriptions[client_id]
    encoded_topic = get_encoded(topic)

    if encoded_topic in client_subscriptions:
        client_subscriptions.remove(topic)
        print 'Topic \'{0}\' successfully cancelled'.format(encoded_topic)

    return create_success_response({
        "success": True
    })


def create_success_response(data):
    return flask.jsonify(data)


def create_invalid_client_id_response(client_id):
    return flask.jsonify({
        "client_id": client_id,
        "success": False,
        "msg": "Invalid client id"
    })


def get_encoded(topic):
    return topic.encode('ascii')


def get_kafka_client():
    return KafkaClient(hosts=app_util.read_conf('Kafka', 'hosts', '127.0.0.1:9092'))


if __name__ == '__main__':
    app.run(debug=True,
            threaded=True,
            port=app_util.read_conf('PushServer', 'port', 5000, int))
