app.directive('successTrendLine', function() {
  return {
    scope: true,
    controller: 'SuccessTrendLineCtrl',
    controllerAs: 'ctrl',
    templateUrl: '/success/trend',
    bindToController: {
        visHeight: '=',
        trendOfSuccessfulResponses: '='
    }
  };
});