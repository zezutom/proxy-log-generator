
angular.module('app', ['nvd3'])
    .controller('appCtrl', function($scope) {

        /** Success vs Error Breakdown **/
        $scope.status_codes = [];
        $scope.status_code_data = [{ values: [], key: 'HTTP Status Codes'}]

        var captureStatusCode = function (data) {
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
                height: 450,
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
        $scope.success_data = [{ values: [], key: 'Successful Responses' }];
        $scope.errors = 0;
        $scope.successes = 0;

        var captureHttpOkRatio = function() {
            if ($scope.errors === 0 && $scope.successes === 0) {
                // This shouldn't happen
                return;
            }
            var total = $scope.successes + $scope.errors;
            var successRatio = $scope.successes / total;
            $scope.success_data[0].values.push({x: total, y: successRatio});
        }

        // HTTP OK Trend
        $scope.success_options = {
            chart: {
                type: 'lineChart',
                height: 180,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 40,
                    left: 55
                },
                x: function(d){ return d.x; },
                y: function(d){ return d.y; },
                yDomain: [0, 1],
                useInteractiveGuideline: true,
                duration: 500,
                yAxis: {
                    tickFormat: function(d){
                       return d3.format('.01f')(d);
                    }
                }
            }
        };

        /** Visit Summary: new visitors vs registered users **/
        $scope.newVisitors = 0;
        $scope.existingUsers = 0;
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
                height: 500,
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

        var subscribe = function(topic, callback) {
            var source = new EventSource('http://localhost:5000/stream/' + topic);
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
        };

        var handleMsg = function(msg) {
            var data = JSON.parse(msg.data);
            captureStatusCode(data);
            captureVisits(data)
            captureHttpOkRatio();
        };

        subscribe('errors', function(msg) {
            $scope.$apply(function() {
                $scope.errors++;
                handleMsg(msg);
            });
        });

        subscribe('success', function(msg) {
            $scope.$apply(function () {
                $scope.successes++;
                handleMsg(msg);
            });
        });
    });