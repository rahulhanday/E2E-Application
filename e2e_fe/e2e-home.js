angular.module("e2e").controller('e2eHomeCtrl', function($scope, $location, $routeParams) {
    $scope.username = $routeParams.username;
});