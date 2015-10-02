angular.module("e2e").controller('e2eLoginCtrl', function($scope, $location, $http) {
    $scope.login = function(user) {
        $http.post('http://localhost:8000/users/login/', {'username': user.username, 'password': user.password})
        .then(function(data){
            $location.path('/home/'+data.data.data.username);
        });
    }

    $scope.forgotPassword = function() {
        //code for forgot password
    }
});