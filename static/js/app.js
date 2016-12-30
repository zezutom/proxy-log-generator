
angular.module('app', ['nvd3'])
    .controller('appCtrl', function($scope) {

        $scope.status_codes = [];
        $scope.http_ok_trend = [{ values: [], key: 'Successful Responses' }];
        $scope.errCount = 0;
        $scope.okCount = 0;

        // HTTP Response Status Summary
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


        var statusCodeData = function() {
            return [
                {
                    'key': 'HTTP Status Codes',
                    'values': $scope.status_codes.sort(compare)
                 }];
        }
        $scope.status_code_data = statusCodeData();

        // Visit Summary: new visitors vs registered users
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

        // HTTP OK Trend
        $scope.http_ok_trend_options = {
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
                },
                xAxis: {
                    tickFormat: function(d){
                       return d3.time.format('%X')(new Date(d));
                    }
                }
            }
        };

        $scope.newVisitorCount = 0;
        $scope.userCount = 0;

        var visitSummaryData = function() {
            return [
                {
                    'label': 'New Visitors',
                    'value': $scope.newVisitorCount
                 },
                 {
                    'label': 'Existing Users',
                    'value': $scope.userCount
                 }
            ];
        }
        $scope.visit_summary_data = visitSummaryData();


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

        var compare = function(a, b) {
            if (a.value < b.value) {
                return 1;
            }
            else if (a.value > b.value) {
                return -1;
            }
            else {
                return 0;
            }
        };

        var captureStatusCode = function (data) {
            var label = data.res_status + '';
            isNew = true;

            for (var i = 0; i < $scope.status_codes.length; i++) {
                var statusCode = $scope.status_codes[i];
                if (statusCode.label === label) {
                    statusCode.value += 1;
                    isNew = false;
                    break;
                }
            }
            if (isNew) {
                $scope.status_codes.push({'label': label, 'value': 1});
            }
            $scope.status_code_data = statusCodeData();
        };

        var captureHttpOkRatio = function() {
            var result = ($scope.errCount === 0 && $scope.okCount === 0) ? 0
                            : $scope.okCount / ( $scope.okCount + $scope.errCount);
            $scope.http_ok_trend[0].values.push({x: +new Date(), y: result});
        }

        subscribe('errors', function(msg) {
            $scope.$apply(function() {
                $scope.errCount++;
                captureStatusCode(JSON.parse(msg.data));
                captureHttpOkRatio();
            });
        });

        subscribe('success', function(msg) {
            $scope.$apply(function () {
                $scope.okCount++;
                var data = JSON.parse(msg.data);
                captureStatusCode(data);
                captureHttpOkRatio();
                if (data.authenticated === '-') {
                    $scope.newVisitorCount++;
                } else {
                    $scope.userCount++;
                }
                $scope.visit_summary_data = visitSummaryData();
            });
        });
    });