
angular.module('app', ['nvd3'])
    .controller('appCtrl', function($scope, $http) {

        /** App Config **/

        // Topic subscriptions
        $scope.serverUrl = 'http://localhost:5000';
        $scope.subscriberId = null;

        // Visualisations
        $scope.visHeight = 300;

        /** Interaction controls **/
        $scope.run = false;
        $scope.sse = null;

        $scope.startStop = function() {
            $scope.run = !$scope.run;
            console.log($scope.run ? 'Started' : 'Stopped');
            if ($scope.run) {
                if (!$scope.subscriberId) {
                    console.log('Registering as a new client');
                    $http.get($scope.serverUrl + '/register')
                        .then(function(response) {
                            var data = response.data;
                            if (data.success) {
                                $scope.subscriberId = data.subscriber_id;
                                console.log('Registration successful, subscriber id: "' + $scope.subscriberId + '"');
                                // Subscribe to start streaming
                                subscribe(function(msg) {
                                    $scope.$apply(function() {
                                        handleMsg(msg);
                                    });
                                });
                            } else {
                                console.error('Registration failed. Try again later.');
                            }
                        });
                } else {
                    // Subscribe to start streaming
                    subscribe(function(msg) {
                        $scope.$apply(function() {
                            handleMsg(msg);
                        });
                    });
                }
            } else {
                // stop streaming
                $http.get($scope.serverUrl + '/unsubscribe/' + $scope.subscriberId + '/proxy_logs')
                    .then(function(response) {
                        console.log('Going to close the subscription');
                        if ($scope.sse) {
                            $scope.sse.close();
                            console.log('Subscription closed.');
                        }
                    });
            }
        };

        /** Initialise (reset) counters **/
        var initCounters = function() {
            $scope.errors = 0;
            $scope.successes = 0;
            $scope.newVisitors = 0;
            $scope.existingUsers = 0;
        }
        initCounters();

        /** Success vs Error Breakdown **/
        $scope.status_codes = [];
        $scope.status_code_data = [{ values: [], key: 'HTTP Status Codes'}]


        var captureStatusCode = function (data) {
            if (data.res_status === 200) {
                $scope.successes++;
            } else {
                $scope.errors++;
            }
            var label = data.res_status + '';
            var status_codes = $scope.status_code_data[0].values;
            isNew = true;

            for (var i = 0; i < status_codes.length; i++) {
                var statusCode = status_codes[i];
                if (statusCode.label === label) {
                    statusCode.value += 1;
                    isNew = false;
                    break;
                }
            }
            if (isNew) {
                status_codes.push({label: label, value: 1});
            }
            status_codes = status_codes.sort(function(a, b) {
                if (a.value < b.value) {
                    return 1;
                }
                else if (a.value > b.value) {
                    return -1;
                }
                else {
                    return 0;
                }
            });
        };

        // NVD3
        $scope.status_code_options = {
            chart: {
                type: 'multiBarHorizontalChart',
                height: $scope.visHeight,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 60,
                    left: 55
                },
                x: function(d){ return d.label; },
                y: function(d){ return d.value; },
                yAxis: {
                    tickFormat: function(d){
                        return d3.format('d')(d);
                    }
                },
                showControls: false,
                showValues: true,
                transitionDuration: 500
            }
        };

        /** Successful Response Trend **/
        $scope.success_data = [];

        var captureHttpOkRatio = function() {
            if ($scope.errors === 0 && $scope.successes === 0) {
                // This shouldn't happen
                return;
            }
            var total = $scope.successes + $scope.errors;
            var successRatio = $scope.successes / total;
            $scope.success_data.push({x: +new Date(), y: successRatio});
        }

        // HTTP OK Trend
        $scope.success_options = {
            chart: {
                type: 'sparklinePlus',
                height: $scope.visHeight,
                x: function(d, i){return i;},
                yDomain: [0, 1],
                xTickFormat: function(d) {
                    return d3.time.format('%X')(new Date($scope.success_data[d].x))
                },
                duration: 250
            }
        };

        /** Visit Summary: new visitors vs registered users **/
        $scope.visit_summary_data = [
                {
                    label: 'New Visitors',
                    value: $scope.newVisitors
                 },
                 {
                    label: 'Existing Users',
                    value: $scope.existingUsers
                 }
            ];
        var captureVisits = function(data) {
            if (data.authenticated === '-') {
                $scope.newVisitors++;
            } else {
                $scope.existingUsers++;
            }
            $scope.visit_summary_data[0].value = $scope.newVisitors;
            $scope.visit_summary_data[1].value = $scope.existingUsers;
        };

        $scope.visit_summary_options = {
            chart: {
                type: 'pieChart',
                height: $scope.visHeight,
                x: function(d){return d.label;},
                y: function(d){return d.value;},
                showLabels: true,
                duration: 500,
                labelThreshold: 0.01,
                labelSunbeamLayout: true,
                legend: {
                    margin: {
                        top: 5,
                        right: 35,
                        bottom: 5,
                        left: 0
                    }
                }
            }
        };


        /** SSE subscription and event handlers **/

        var subscribe = function(callback) {
            var source = new EventSource($scope.serverUrl + '/subscribe/' + $scope.clientId + '/proxy_logs');
            source.addEventListener('message', callback, false);
            source.addEventListener('open', function(e) {
                console.log('Opening a new connection');
            }, false);
            source.addEventListener('error', function(e) {
                console.log('There was an error!');
                if (e.readyState == EventSource.CLOSED) {
                    console.log('Server closed the connection! Terminating..')
                    source.close();
                }
            }, false);
            $scope.sse = source;
            console.log('Successfully subscribed')
        };

        var handleMsg = function(msg) {
            var data = JSON.parse(msg.data);
            captureStatusCode(data);
            captureVisits(data)
            captureHttpOkRatio();
        };

        setInterval(function() {
            if (!$scope.run) return;
            initCounters();
        }, 5000);
    });