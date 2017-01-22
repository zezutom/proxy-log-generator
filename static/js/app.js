var app = angular.module('app', ['nvd3']);
app
    .controller('AppCtrl', ['$scope', 'subscriberService', 'dashboardService',
    function($scope, subscriberService, dashboardService) {

        /** Shared state **/
        $scope.run = false;
        $scope.visHeight = 250;

        /** Dashboard Visualisations **/
        $scope.successfulResponseTrendGraphData = dashboardService.getSuccessfulResponseTrendGraphData();
        $scope.statusCodeGraphData = dashboardService.getStatusCodeGraphData();
        $scope.visitSummaryGraphData = dashboardService.getVisitSummaryGraphData();

        /** Internal state **/
        var subscriberId = null;

        var subscribe = function() {
            subscriberService.subscribe(subscriberId, function(msg) {
                $scope.$apply(function() {
                    dashboardService.parseMessage(msg);
                });
            });
        };

        /** App controls **/
        $scope.startStop = function() {
            $scope.run = !$scope.run;
            if ($scope.run) {
                if ($scope.subscriberId) {
                    // Subscribe to the topic
                    subscribe();
                } else {
                    // Register and subscribe
                    subscriberService.register()
                        .then(
                            function(response) {
                                var data = response.data;
                                if (data.success) {
                                    subscriberId = data.subscriber_id;
                                    subscribe();
                                }
                            }
                        );
                }
            } else {
                // Stop streaming (unsubscribe)
                if (subscriberId) {
                    subscriberService.unsubscribe(subscriberId);
                }
            }
        };

        // Reset counters every 5 seconds to make the output more dynamic
        setInterval(function() {
            if (!$scope.run) return;
            dashboardService.init();
        }, 5000);
    }])
    .factory('subscriberService', ['$http', function($http) {
        return new SubscriberService($http);
    }])
    .factory('dashboardService', function() {
        return new DashboardService();
    });