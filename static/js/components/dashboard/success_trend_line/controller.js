app.controller('SuccessTrendLineCtrl', ['$scope', function($scope) {
    $scope.options = {
        chart: {
            type: 'sparklinePlus',
            height: 250,
            x: function(d, i){return i;},
            yDomain: [0, 1],
            xTickFormat: function(d) {
                return d3.time.format('%X')(new Date($scope.successfulResponseTrendGraphData[d].x))
            },
            duration: 250
        }
    };
}]);