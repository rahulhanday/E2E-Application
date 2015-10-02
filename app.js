angular.module("e2e", ["ngRoute"]).config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/path', {
            templateUrl: '',
            controller: ''
        }).
        otherwise({
            templateUrl: 'e2e_fe/e2e-login.html',
            controller: 'e2eLoginCtrl'
        });
    }
]);