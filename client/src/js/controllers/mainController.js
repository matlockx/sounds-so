(function() {
    angular.module('app').controller('mainCtrl', ['$scope', 'Sound', function($scope, Sound) {
        $scope.search = '';
        $scope.sound = '';

        $scope.soundFile = {};

        $scope.searchSound = function () {
            Sound.get({like: $scope.search}, function(sound) {
                $scope.sound = sound;
                $scope.soundFile = new Howl({
                    urls: [sound.url]
                });
            });
        };

        $scope.play = function() {
            $scope.soundFile.play();
        };

        $scope.pause = function() {
            $scope.soundFile.pause();
        };

        $scope.stop = function() {
            $scope.soundFile.stop();
        };

    }]);
})();
