(function() {
  angular.module('app').controller('mainCtrl', ['$scope', '$routeParams', '$location', 'Sound',
  function($scope, $routeParams, $location, Sound) {
    $scope.search = $routeParams.query || "";
    $scope.sound = null;
    $scope.howl = null;

    function playSound(sound) {
      $scope.stop();
      $scope.sound = sound;
      $scope.howl = new Howl({
        urls: [sound.url],
        autoplay: true,
        loop: true
      });
    }

    function performSearch() {
      Sound.get({like: $scope.search}, function(sound) {
        if(sound.url) {
          playSound(sound);
        } else {
          $scope.no_result = true;
        }
      });
    }

    $scope.$on('$destroy', function () {
      $scope.stop();
    });

    $scope.searchSound = function () {
      $scope.stop();
      $location.path("/" + $scope.search);
    };

    $scope.stop = function() {
      if($scope.howl != null) {
        $scope.howl.stop();
      }
    };

    // start a search if we have a query.
    if($scope.search && $scope.search != "") {
      performSearch();
    }
  }]);
})();
