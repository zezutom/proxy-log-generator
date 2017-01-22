var app = angular.module('app', ['nvd3']);
app
    .controller('AppCtrl', ['$scope', 'appService', 'subscriberService',
    function($scope, appService, subscriberService) {

        /** Shared state **/
        $scope.run = false;
        $scope.visHeight = 250;

        /** Initialise (reset) counters **/
        var initCounters = function() {
            $scope.errors = 0;
            $scope.successes = 0;
            $scope.newVisitors = 0;
            $scope.existingUsers = 0;
        }
        initCounters();

        // Successful Response Trend
        $scope.trendOfSuccessfulResponses = [];

        // Success vs Error Breakdown
        $scope.statusCodes = [];
        $scope.statusCodeData = [{ values: [], key: 'HTTP Status Codes'}]

        // Visit Summary: new visitors vs registered users
        $scope.visitSummaryData = [
            {
                label: 'New Visitors',
                value: $scope.newVisitors
             },
             {
                label: 'Existing Users',
                value: $scope.existingUsers
             }
        ];
        /** Internal state **/
        var subscriberId = null;

        var updateTrendOfSuccessfulResponses = function() {
            var successRatio = appService.calculateRatio($scope.successes, $scope.errors);
            $scope.trendOfSuccessfulResponses.push(successRatio);
        };

        var captureVisits = function() {
            $scope.visitSummaryData[0].value = $scope.newVisitors;
            $scope.visitSummaryData[1].value = $scope.existingUsers;
        };

        var handleMsg = function(msg) {
            if (appService.isSuccess(msg)) {
                $scope.successes++;
            } else {
                $scope.errors++;
            }
            if (appService.isAuthenticated(msg)) {
                $scope.existingUsers++;
            } else {
                $scope.newVisitors++;
            }
            updateTrendOfSuccessfulResponses();
            captureVisits();
            $scope.statusCodes = appService.updateStatusCodes(msg, $scope.statusCodeData[0].values);
        };

        var subscribe = function() {
            subscriberService.subscribe(subscriberId, function(msg) {
                $scope.$apply(function() {
                    handleMsg(msg);
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
            initCounters();
        }, 5000);
    }])
    .factory('subscriberService', ['$http', function($http) {
        return new SubscriberService($http);
    }])
    .factory('appService', function() {
        return new AppService();
    });