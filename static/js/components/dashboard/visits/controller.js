app.controller('VisitorsCtrl', ['$scope', function($scope) {
    $scope.options = {
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
}]);