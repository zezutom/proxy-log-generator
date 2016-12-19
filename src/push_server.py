#! /usr/bin/python

import json
from time import sleep

import flask
from flask import Flask
from flask.ext.cors import CORS, cross_origin
from kafka import KafkaConsumer

app = Flask(__name__)
cors = CORS(app, resources={r"/stream": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

consumer = KafkaConsumer('all_logs')


@app.route('/stream')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def stream():
    def stream_events():
        for msg in consumer:
            log = json.loads(msg.value)
            user = log.get('authenticated', '-')

            event = dict(success=True if log.get('res_status') == 200 else False, user=user,
                         anonymous=True if user == '-' else False, url=log.get('url'))

            # Wait to give a client a chance to react
            sleep(1)

            # Stream the new message
            yield "data: {}\n\n".format(json.dumps(event))

    return flask.Response(stream_events(), mimetype="text/event-stream")



if __name__ == '__main__':
    app.run(debug=True)