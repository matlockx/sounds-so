(function () {
  'use strict';
  angular.module('app').config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'src/views/main.html',
        controller: 'mainCtrl'
      })
      .when("/:query", {
        templateUrl: 'src/views/main.html',
        controller: 'mainCtrl'
      })
      .otherwise({redirectTo: '/'});
  }]);
})();
