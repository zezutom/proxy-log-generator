app.directive('statusCodesBarChart', function() {
    console.log('Invoking the trendLine directive');
  return {
    scope: true,
    controller: 'StatusCodesCtrl',
    controllerAs: 'ctrl',
    templateUrl: '/status/codes',
    bindToController: {
        visHeight: '=',
        trendOfSuccessfulResponses: '='
    }
  };
});