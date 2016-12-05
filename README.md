[![Build Status](https://travis-ci.org/zezutom/proxy-log-generator.svg?branch=master)](https://travis-ci.org/zezutom/proxy-log-generator)
[![Coverage Status](https://coveralls.io/repos/github/zezutom/proxy-log-generator/badge.svg)](https://coveralls.io/github/zezutom/proxy-log-generator)
# Proxy Log Generator
The app is a simple Python script which generates a fake web server log. Unsurprisingly, the script comes with a bunch of configuration options allowing to control data volumes and variety. The project has been inspired by some outstanding examples, see [Resources](#resources) for details. 

## Example Output
```
2016-07-15 22:34:48	181.42.40.22	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17	clay.richard	http://www.raymondelliott.com/659.html	200	2718553
2016-07-15 22:40:36	58.75.187.70	Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0	elisa.wilcox	https://www.kendall-sparks.com/839/193/287/766.jpg	302	986709
2016-07-15 22:46:29	104.213.217.249	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36	thomas.henry	http://www.erika-hatfield.com/327/711/168/786.php	404	1822779
2016-07-15 22:52:00	7.46.154.248	Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0	latasha.byers	https://www.shaun-dyer.com/888/187/252/296.jpg	200	4580341
2016-07-15 22:57:46	177.111.138.63	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17	-	http://www.sheila-branch.com/530/766/327.html	404	606885
2016-07-15 23:02:51	60.141.239.58	Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46	caroline.cole	https://www.michael-hampton.com/708/910.php	404	3818970
2016-07-15 23:08:29	37.113.174.59	Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36	mandy.gibson	https://www.arielberg.com/752/413/849/808.png	404	1055575
2016-07-15 23:14:25	108.180.117.206	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36	isaiah.anderson	http://www.estebanfinley.com/380/46/277.html	404	2998959
2016-07-15 23:19:35	145.181.244.114	Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36	-	http://www.carolrocha.com/744.html	404	3960244
2016-07-15 23:25:28	83.90.177.209	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36	-	https://www.lindsay-barron.com/932/685.html	200	159664
```
See [the full log file](examples/logfile.log).

## Usage
### Streaming
Continuously generate logs into either a console or a specified remote endpoint. 

Stream logs to a console at a rate of 100 ms a message.
```
python src/log_generator.py --stream 100
```
Stream logs to a HTTP server (_protocol://host:port/endpoint_) at a rate of 100 ms a message.
```
python src/log_generator.py --stream 100 --url http://localhost:8081/contentListener
```
Also, when streamed via HTTP, the logs are turned into JSON for an easier parsing and analysis.
```
{"authenticated": "cameron.henry", "url": "http://www.chelsea-mcintyre.com/586/869/374.png", "timestamp": "2016-12-05 07:47:59", "user_agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", "ip": "163.54.250.17", "res_status": "302", "res_size": 1881216}
{"authenticated": "-", "url": "https://www.catherinesnyder.com/592.png", "timestamp": "2016-12-05 07:47:59", "user_agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36", "ip": "250.67.114.5", "res_status": "200", "res_size": 1653259}
```
### Normal daily traffic
No additional arguments needed. The output file will be saved in the current working directory as _logfile.log_.

To override the file name and location: _-f_ or _--file_
```
python src/log_generator.py --file [path to a log file]
```

### Normal traffic for a specified period of time
_-t_ or _--time_, 1 day by default

Please note, to make the output more realistic times are approximate, i.e. they center around the requested time period or frequency. However, no exact match is guaranteed. In fact, it is not even desirable.
```
python src/log_generator.py --time [number of days (d), hours (h), minutes (m), seconds (s) or milliseconds (ms)]
```
Examples:
```
# 2 days
python src/log_generator.py --time 2d

# 5 hours
python src/log_generator.py --time 5h

# half an hour
python src/log_generator.py --time 30m

# 15 seconds
python src/log_generator.py --time 15s

# 100 milliseconds
python src/log_generator.py --time 100ms
```

### Define frequency of inbound events
_-i_ or _--increment_, every 5 minutes by default
```
python src/log_generator.py --increment [every X minutes (m), seconds (s) or milliseconds (ms)]
```
Examples:
```
# A new request every minute
python src/log_generator.py --increment 1m

# A new request every 10 seconds
python src/log_generator.py --increment 10s

# About 10 requests per second
python src/log_generator.py --increment 100ms
```
### Concurrent connections
The overall volume is determined by a number of concurrent requests. Use _-v_ or _--volume_ to define what is perceived as a normal load. 100 simultaneous requests are generated by default.

Examples:
```
# 10 concurrent requests
python src/log_generator.py --volume 10

# 1000 concurrent requests for a limited period of time
python src/log_generator.py --volume 1000 --time 1h
```

## Resources
* [Hortonworks' Hadoop Tutorials, Tutorial 12: Refining and Visualizing Server Log Data](https://github.com/hortonworks/hadoop-tutorials/blob/master/Sandbox/T12_Refining_and_Visualizing_Server_Log_Data.md)
* [Bitsinfo Log Generator](https://github.com/bitsofinfo/log-generator)
* [Paul Poputa-Clean's Ruby Log Generator](https://github.com/paulpc/LogGenerator)





