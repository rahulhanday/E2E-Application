angular.module("e2e").controller('e2eLoginCtrl', function($scope, $location, $http) {
    $scope.login = function(user) {
        $http.post('http://localhost:8000/users/login/', {'username': user.username, 'password': user.password})
        .then(function(data){

        });
    }

    $scope.forgotPassword = function() {

    }
});