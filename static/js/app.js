
angular.module('app', [])
    .controller('appCtrl', function($scope) {

        // count messages by categories: registered users, new anonymous visitors and errors
        $scope.userCount = 0;
        $scope.anonymousCount = 0;
        $scope.errCount = 0;

        // handles the callback from the received event
        var handleCallback = function (msg) {
            $scope.$apply(function () {
                var data = JSON.parse(msg.data);
                if (data['success']) {
                    if (data['anonymous']) $scope.anonymousCount++;
                    else $scope.userCount++;
                } else {
                    $scope.errCount++;
                }
            });
        }

        var source = new EventSource('/stream');
        source.addEventListener('message', handleCallback, false);
    });