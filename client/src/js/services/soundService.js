(function () {
    'use strict';

    angular.module('app')
        .factory('Sound', ['$resource',function ($resource) {
            return $resource('http://95.138.174.122/api/v1/random/sound');
        }]);
})();
