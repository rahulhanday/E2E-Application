angular.module("e2e").controller('e2eLoginCtrl', function($scope, $location) {
    $scope.login = function() {
        $location.path('/home');
    }

    $scope.forgotPassword = function() {

    }
});