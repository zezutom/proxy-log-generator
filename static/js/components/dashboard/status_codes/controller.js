app.controller('StatusCodesCtrl', ['$scope', function($scope) {
    $scope.options = {
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
}]);