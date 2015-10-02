angular.module("e2e", ["ngRoute"]).config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/login/', {
            templateUrl: 'e2e_fe/e2e-login.html',
            controller: 'e2eLoginCtrl'
        }).
        when('/home', {
            templateUrl: 'e2e_fe/e2e-home.html',
            controller: 'e2eHomeCtrl'
        }).
        otherwise({
            redirectTo:'login/'
        });
    }
]);