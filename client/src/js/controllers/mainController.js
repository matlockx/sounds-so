(function() {
    angular.module('app').controller('mainCtrl', ['$scope', 'Sound', function($scope, Sound) {
        $scope.search = '';
        $scope.sound = '';

        $scope.soundFile = {};

        $scope.playing = false;

        $scope.searchSound = function () {
            Sound.get({like: $scope.search}, function(sound) {
                $scope.sound = sound;
                $scope.soundFile = new Howl({
                    urls: [sound.url],
                    onend: function() {
                        $scope.playing = false;
                    }
                });
            });
        };

        $scope.play = function() {
            if(!$scope.playing) {
                $scope.playing = true;
                $scope.soundFile.play();
            }
        };

        $scope.pause = function() {
            $scope.playing = false;
            $scope.soundFile.pause();
        };

        $scope.stop = function() {
            $scope.playing = false;
            $scope.soundFile.stop();
        };

    }]);
})();
