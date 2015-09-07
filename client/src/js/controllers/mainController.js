(function() {
  angular.module('app').controller('mainCtrl', ['$scope', '$routeParams', '$location', 'Sound',
  function($scope, $routeParams, $location, Sound) {
    $scope.search = $routeParams.query || "";
    $scope.sound = null;
    $scope.howl = null;
    $scope.searching = false;
    $scope.searchTermWidth = 0;

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
      $scope.searching = true;
      $scope.lastSearch = $scope.search;

      Sound.get({like: $scope.search}, function(sound) {
        $scope.searching = false;

        if (sound.url) {
          playSound(sound);
          $scope.noResult = false;
        } else {
          $scope.noResult = true;
        }
      });
    }

    function measureText(text) {
      return jQuery("#searchGhost").text(text).width();
    }

    function onSearchTermChanged() {
      if($scope.search == "") {
        $scope.search = "";
        $scope.searchTermWidth = measureText("anything");
      } else {
        $scope.searchTermWidth = measureText($scope.search);
      }
    }

    $scope.$on('$destroy', function () {
      $scope.stop();
    });

    $scope.searchSound = function () {
      $scope.stop();

      if($scope.search === $scope.lastSearch) {
        performSearch();
      } else {
        $location.path("/" + $scope.search);
      }
    };

    $scope.stop = function() {
      if($scope.howl != null) {
        $scope.howl.stop();
      }
    };

    $scope.$watch("search", onSearchTermChanged);

    jQuery(window).resize(function() {
      onSearchTermChanged();
      $scope.$apply();
    });

    // start a search if we have a query.
    if($scope.search && $scope.search !== "") {
      performSearch();
    }

    window.setTimeout(function() {
      onSearchTermChanged();
      $scope.$apply();
    }, 500);
  }]);
})();
