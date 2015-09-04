(function () {
  'use strict';

  angular.module('app')
    .factory('Sound', ['$resource',function ($resource) {
      return $resource('http://sounds.so/api/v1/random/sound');
    }]);
})();
