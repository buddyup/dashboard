var buddyupDashboard = angular.module('buddyupDashboard', ['ngRoute']);

buddyupDashboard.config(function($routeProvider, $sceDelegateProvider) {
    $routeProvider

        // route for the dashboard page
        .when('/', {
            templateUrl : window.STATIC_URL + 'main_site/js/pages/dashboard.html',
            controller  : 'mainController'
        })
        // // route for another page
        // .when('/another', {
        //     templateUrl : 'pages/another.html',
        //     controller  : 'anotherController'
        // })

     $sceDelegateProvider.resourceUrlWhitelist([
        // Allow same origin resource loads.
        'self',
        // Allow loading from our assets domain.  Notice the difference between * and **.
        window.STATIC_URL + '/**'
    ]);
});

buddyupDashboard.controller('mainController', function($scope) {
    // create a message to display in our view
    function sort_events(a,b) {
      if (a.recorded_at > b.recorded_at)
         return -1;
      if (a.recorded_at < b.recorded_at)
        return 1;
      return 0;
    }
    $scope.update_display_data = function() {
        $scope.create_combined();
        $scope.create_averaged();
        if ($scope.aggregate) {
            $scope.display_dataset = $scope.averaged;
        } else {
            $scope.display_dataset = $scope.combined;
        }
        console.log($scope.display_dataset)
    }
    $scope.create_combined = function() {
        $scope.combined = [];
        if ($scope.sample_type == "percentages") {
            var d;
            for (var d_index in $scope.data_points) {
                d = angular.copy($scope.data_points[d_index]);
                d["num_active_users"] = (100 * d["num_active_users"] / d["num_total_users"]).toFixed(0);
                d["num_authenticated"] = (100 * d["num_authenticated"] / d["num_total_users"]).toFixed(0);
                d["num_filled_in_profile"] = (100 * d["num_filled_in_profile"] / d["num_total_users"]).toFixed(0);
                d["num_hit_home_page"] = (100 * d["num_hit_home_page"] / d["num_total_users"]).toFixed(0);
                d["num_with_one_class"] = (100 * d["num_with_one_class"] / d["num_total_users"]).toFixed(0);
                d["num_with_one_buddy"] = (100 * d["num_with_one_buddy"] / d["num_total_users"]).toFixed(0);
                d["num_attended_one_event"] = (100 * d["num_attended_one_event"] / d["num_total_users"]).toFixed(0);
                $scope.combined.push(d);
            }
        } else {
            $scope.combined = $scope.combined.concat($scope.data_points)
        }
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
        $scope.combined.sort(sort_events);
    }
    $scope.create_averaged = function() {
        $scope.averaged = [];

        function reset_aggregates() {
            num_samples = 0;
            num_total_users = 0;
            num_active_users = 0;
            num_authenticated = 0;
            num_filled_in_profile = 0;
            num_hit_home_page = 0;
            num_with_one_class = 0;
            num_with_one_buddy = 0;
            num_attended_one_event = 0;
            buddy_ratio = 0;
        }

        var num_samples, num_total_users, num_active_users,
            num_authenticated, num_filled_in_profile, num_hit_home_page,
            num_with_one_class, num_with_one_buddy,
            num_attended_one_event, buddy_ratio;
        
        reset_aggregates();
        var start_date = $scope.combined[0].display_date;

        // Assumes combined has been created.
        for (var m_index in $scope.combined) {
            m = $scope.combined[m_index];
            console.log("buddy_ratio" + buddy_ratio)
            console.log("num_samples" + num_samples)

            if (m.type == "event" || m.type == "code_push") {
                buddy_ratio_to_save = buddy_ratio / num_samples.toFixed(0);
                if ($scope.sample_type == "percentages") {
                    num_samples = num_samples / 100
                }
                if (num_samples > 0) {
                    $scope.averaged.push({
                        "type": "data_point",
                        "display_date": start_date + " - " + m.display_date,
                        "num_total_users": (num_total_users / num_samples).toFixed(0),
                        "num_active_users": (num_active_users / num_samples).toFixed(0),
                        "num_authenticated": (num_authenticated / num_samples).toFixed(0),
                        "num_filled_in_profile": (num_filled_in_profile / num_samples).toFixed(0),
                        "num_hit_home_page": (num_hit_home_page / num_samples).toFixed(0),
                        "num_with_one_class": (num_with_one_class / num_samples).toFixed(0),
                        "num_with_one_buddy": (num_with_one_buddy / num_samples).toFixed(0),
                        "num_attended_one_event": (num_attended_one_event / num_samples).toFixed(0),
                        "buddy_ratio": buddy_ratio_to_save
                    });
                }
                $scope.averaged.push(m);
                reset_aggregates();
            } else {
                num_samples += 1;
                if ($scope.sample_type == "percentages") {
                    num_total_users += m.num_total_users / 100;
                    num_active_users += m.num_active_users / 100;
                    num_authenticated += m.num_authenticated / 100;
                    num_filled_in_profile += m.num_filled_in_profile / 100;
                    num_hit_home_page += m.num_hit_home_page / 100;
                    num_with_one_class += m.num_with_one_class / 100;
                    num_with_one_buddy += m.num_with_one_buddy / 100;
                    num_attended_one_event += m.num_attended_one_event / 100;
                } else {
                    num_total_users += m.num_total_users;
                    num_active_users += m.num_active_users;
                    num_authenticated += m.num_authenticated;
                    num_filled_in_profile += m.num_filled_in_profile;
                    num_hit_home_page += m.num_hit_home_page;
                    num_with_one_class += m.num_with_one_class;
                    num_with_one_buddy += m.num_with_one_buddy;
                    num_attended_one_event += m.num_attended_one_event;
                }
                buddy_ratio += m.buddy_ratio;
            }
        }
        if (num_samples > 0) {
            $scope.averaged.push({
                "type": "data_point",
                "display_date": start_date + " - " + m.display_date,
                "num_total_users": (num_total_users / num_samples).toFixed(0),
                "num_active_users": (num_active_users / num_samples).toFixed(0),
                "num_authenticated": (num_authenticated / num_samples).toFixed(0),
                "num_filled_in_profile": (num_filled_in_profile / num_samples).toFixed(0),
                "num_hit_home_page": (num_hit_home_page / num_samples).toFixed(0),
                "num_with_one_class": (num_with_one_class / num_samples).toFixed(0),
                "num_with_one_buddy": (num_with_one_buddy / num_samples).toFixed(0),
                "num_attended_one_event": (num_attended_one_event / num_samples).toFixed(0),
                "buddy_ratio": (100 * buddy_ratio / num_samples).toFixed(0) + "%"
            });
        }
        $scope.averaged.sort(sort_events);
    }

    console.log(window.dashboardData)
    $scope.init_dashboard = function() {
        $scope.show_events = true;
        $scope.show_code_pushes = true;
        $scope.sample_type = "raw_data"

        $scope.message = 'Hello, world!';
        $scope.data_points = window.dashboardData.data_points;
        $scope.milestones = window.dashboardData.milestones;
        
        $scope.update_display_data();
    }
});