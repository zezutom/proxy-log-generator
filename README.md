[![Build Status](https://travis-ci.org/zezutom/proxy-log-generator.svg?branch=master)](https://travis-ci.org/zezutom/proxy-log-generator)
[![Coverage Status](https://coveralls.io/repos/github/zezutom/proxy-log-generator/badge.svg)](https://coveralls.io/github/zezutom/proxy-log-generator)
# Proxy Log Generator
Streams fake web server logs. Primarily intended for testing of streaming with NiFi and Kafka.

## In a Nutshell
* Simulates a continuous web traffic, see an example
* Generated logs are streamed to an HTTP endpoint
* Locust UI for load configuration
* Extensible, ships with NiFi and Kafka integration

## Example Output
```
{'authenticated': 'antoine.dickerson', 'url': 'https://www.christywatts.com/735/201.php', 'timestamp': '2016-12-24 16:50:08', 'user_agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0', 'ip': '53.143.50.131', 'res_status': 404, 'res_size': 4129136}
{'authenticated': 'patrice.camacho', 'url': 'http://www.austinwalker.com/981.png', 'timestamp': '2016-12-24 16:50:08', 'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36', 'ip': '48.26.166.195', 'res_status': 200, 'res_size': 590813}
{'authenticated': 'maurice.francis', 'url': 'https://www.frankie-paul.com/182.php', 'timestamp': '2016-12-24 16:50:08', 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36', 'ip': '117.45.110.155', 'res_status': 200, 'res_size': 3103266}
{'authenticated': '-', 'url': 'https://www.nicolemckinney.com/631/784/669/591.html', 'timestamp': '2016-12-24 16:50:08', 'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0', 'ip': '66.220.33.180', 'res_status': 404, 'res_size': 1812680}
{'authenticated': '-', 'url': 'https://www.abbeyhickman.com/391.jpg', 'timestamp': '2016-12-24 16:50:08', 'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 'ip': '181.196.3.20', 'res_status': 200, 'res_size': 1598792}
```

## Dependencies
* [Locust 0.7.5](http://locust.io/)
* [NiFi 1.0.0](https://nifi.apache.org/)
* [Kafka 2.11_0.10.1.0](https://kafka.apache.org/)
* [Python 2.7](https://www.python.org/download/releases/2.7.2/)
* [Angular-nvD3 1.0.9](https://krispo.github.io/angular-nvd3/)

## Installation
```
pip install --user -r requirements.txt && bower install
```

## Usage
A local installation of Kafka and NiFi is assumed at the moment. Please check [log_generator.sh](log_generator.sh)
and amend this section as needed.
```bash
init() {
    NIFI_HOME=~/nifi-1.0.0
    KAFKA_HOME=~/kafka_2.11-0.10.1.0
}
```
Start NiFi, Kafka and Locust UI by running the script below.
```bash
sh ./log_generator.sh start
```
Import a [Streaming Example template](https://github.com/zezutom/NiFiByExample/blob/master/templates/streaming/web_proxy_analysis.xml) to NiFi,
start all processors.

Next, open up Locust UI at http://localhost:8089 and define how hard to you wish to hit the NiFi listener with generated logs.

TODO - add screenshot

Trigger the load and observe the streaming pipeline in NiFi.

TODO - add screenshot

Open up a Dashboard at http://localhost:3000 and observe changing log aggregations.

TODO - add screenshot

# Architecture
TODO





