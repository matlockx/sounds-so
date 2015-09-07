(function() {
  'use strict';

    var app = angular.module('app', ['ngRoute', 'ngResource']);

    app.directive('autofocus', ['$timeout',function ($timeout) {
      return {
        restrict: 'A',
        link: function ($scope, $element) {
          $timeout(function () {
            $element[0].focus();
          });
        }
      };
    }
  ]);
})();
