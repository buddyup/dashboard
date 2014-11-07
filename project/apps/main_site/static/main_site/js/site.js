var buddyupDashboard = angular.module('buddyupDashboard', ['ngRoute']);

buddyupDashboard.config(function($routeProvider) {
    $routeProvider

        // route for the dashboard page
        .when('/', {
            templateUrl : 'static/main_site/js/pages/dashboard.html',
            controller  : 'mainController'
        })

        // // route for another page
        // .when('/another', {
        //     templateUrl : 'pages/another.html',
        //     controller  : 'anotherController'
        // })
});

buddyupDashboard.controller('mainController', function($scope) {
    // create a message to display in our view
    function sort_events(a,b) {
      if (a.recorded_at < b.recorded_at)
         return -1;
      if (a.recorded_at > b.recorded_at)
        return 1;
      return 0;
    }
    $scope.create_combined = function() {
        $scope.combined = $scope.data_points;
        var m;
        for (var m_index in $scope.milestones) {
            m = $scope.milestones[m_index];
            if (m.type == "code_push" && $scope.show_code_pushes) {
                $scope.combined.push(m);
            } else {
                if (m.type == "event" && $scope.show_events) {
                    $scope.combined.push(m);
                }
            }
        }
        // $scope.combined.concat($scope.milestones);
        $scope.combined.sort(sort_events);
        console.log($scope.combined)
    }

    console.log(window.dashboardData)
    $scope.init_dashboard = function() {
        $scope.show_events = true;
        $scope.show_code_pushes = true;

        $scope.message = 'Hello, world!';
        $scope.data_points = window.dashboardData.data_points;
        $scope.milestones = window.dashboardData.milestones;
        
        $scope.create_combined();
    }
});