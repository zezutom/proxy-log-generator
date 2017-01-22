app.directive('statusCodesBarChart', function() {
  return {
    scope: true,
    controller: 'StatusCodesCtrl',
    controllerAs: 'ctrl',
    templateUrl: '/status/codes',
    bindToController: {
        visHeight: '='
    }
  };
});