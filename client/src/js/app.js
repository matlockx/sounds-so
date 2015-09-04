(function() {
  'use strict';

    angular.module('utils.autofocus', []).directive('autofocus', ['$timeout',
      function ($timeout) {
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

  angular.module('app', ['ngRoute', 'ngResource', 'ui.bootstrap']);

})();
