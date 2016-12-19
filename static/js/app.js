
angular.module('app', ['nvd3'])
    .controller('appCtrl', function($scope) {

        // count messages by categories: registered users, new anonymous visitors and errors
        $scope.userCount = 0;
        $scope.anonymousCount = 0;
        $scope.errCount = 0;

        // nvd3
        $scope.options = {
            chart: {
                type: 'discreteBarChart',
                height: 450,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 60,
                    left: 55
                },
                x: function(d){ return  d.value + ' ' + d.label; },
                y: function(d){ return d.ratio; },
                yDomain: [0, 100],
                showValues: true,
                valueFormat: function(d){
                    return d3.format(',.2f')(d);
                },
                transitionDuration: 500,
                yAxis: {
                    axisLabelDistance: 10
                }
            }
        };

        var currentData = function() {
            var total = $scope.userCount + $scope.anonymousCount + $scope.errCount;
            var percent = function(value) { return total === 0 ? 0 : (value / total) * 100; }
            return [
                {
                    key: 'Website Traffic',
                    values: [
                        {'label': 'users', 'value': $scope.userCount, 'ratio': percent($scope.userCount)},
                        {'label': 'visitors', 'value': $scope.anonymousCount, 'ratio': percent($scope.anonymousCount)},
                        {'label': 'errors', 'value': $scope.errCount, 'ratio': percent($scope.errCount)}
                    ]
                 }];
        }

        // Visualised stats about website visits
        $scope.data = currentData();

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

        subscribe('auth', function(msg) {
            $scope.$apply(function () {
                $scope.userCount++;
                $scope.data = currentData();
            });
        });

        subscribe('anon', function(msg) {
            $scope.$apply(function () {
                $scope.anonymousCount++;
                $scope.data = currentData();
            });
        });

        subscribe('err', function(msg) {
            $scope.$apply(function () {
                $scope.errCount++;
                $scope.data = currentData();
            });
        });
    });