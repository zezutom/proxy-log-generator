app.directive('visitSummaryPieChart', function() {
  return {
    scope: true,
    controller: 'VisitorsCtrl',
    controllerAs: 'ctrl',
    templateUrl: '/visit/summary',
    bindToController: {
        visHeight: '=',
        trendOfSuccessfulResponses: '='
    }
  };
});