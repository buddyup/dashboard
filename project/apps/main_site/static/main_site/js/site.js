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
        window.STATIC_URL + '**'
    ]);
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
    $scope.update_display_data = function() {
        $scope.create_combined();
        if ($scope.aggregate) {
            $scope.create_averaged();
            $scope.display_dataset = $scope.averaged;
        } else {
            $scope.display_dataset = $scope.combined;
        }
    }
    $scope.create_combined = function() {
        $scope.combined = [];
        if ($scope.sample_type == "funneled" && !$scope.aggregate) {
            var d;
            for (var d_index in $scope.data_points) {
                d = angular.copy($scope.data_points[d_index]);
                orig = angular.copy($scope.data_points[d_index]);
                d["num_active_users"] = Math.round(100 * d["num_active_users"] / orig["num_total_users"]);
                d["num_authenticated"] = Math.round(100 * d["num_authenticated"] / orig["num_active_users"]);
                d["num_filled_in_profile"] = Math.round(100 * d["num_filled_in_profile"] / orig["num_authenticated"]);
                d["num_hit_home_page"] = Math.round(100 * d["num_hit_home_page"] / orig["num_filled_in_profile"]);
                d["num_with_one_class"] = Math.round(100 * d["num_with_one_class"] / orig["num_hit_home_page"]);
                d["num_with_one_buddy"] = Math.round(100 * d["num_with_one_buddy"] / orig["num_with_one_class"]);
                d["num_attended_one_event"] = Math.round(100 * d["num_attended_one_event"] / orig["num_with_one_buddy"]);
                $scope.combined.push(d);
            }
        } else {
            if ($scope.sample_type == "percentages" && !$scope.aggregate) {
                var d;
                for (var d_index in $scope.data_points) {
                    d = angular.copy($scope.data_points[d_index]);
                    d["num_active_users"] = Math.round(100 * d["num_active_users"] / d["num_total_users"]);
                    d["num_authenticated"] = Math.round(100 * d["num_authenticated"] / d["num_total_users"]);
                    d["num_filled_in_profile"] = Math.round(100 * d["num_filled_in_profile"] / d["num_total_users"]);
                    d["num_hit_home_page"] = Math.round(100 * d["num_hit_home_page"] / d["num_total_users"]);
                    d["num_with_one_class"] = Math.round(100 * d["num_with_one_class"] / d["num_total_users"]);
                    d["num_with_one_buddy"] = Math.round(100 * d["num_with_one_buddy"] / d["num_total_users"]);
                    d["num_attended_one_event"] = Math.round(100 * d["num_attended_one_event"] / d["num_total_users"]);
                    $scope.combined.push(d);
                }
            } else {
                $scope.combined = $scope.combined.concat($scope.data_points)
            }
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
        $scope.combined.sort(sort_events).reverse();
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
        function make_data_point() {
            var data = {
                "type": "data_point",
                "display_date": m.display_date + " - " + start_date,
                "buddy_ratio": buddy_ratio_to_save,
            }
            if (last_averaged_point != false) {
                data["num_total_users"] = Math.round((1.0*num_total_users / num_samples) - (last_averaged_point.num_total_users));
                data["num_active_users"] = Math.round((1.0*num_active_users / num_samples) - (last_averaged_point.num_active_users));
                data["num_authenticated"] = Math.round((1.0*num_authenticated / num_samples) - (last_averaged_point.num_authenticated));
                data["num_filled_in_profile"] = Math.round((1.0*num_filled_in_profile / num_samples) - (last_averaged_point.num_filled_in_profile));
                data["num_hit_home_page"] = Math.round((1.0*num_hit_home_page / num_samples) - (last_averaged_point.num_hit_home_page));
                data["num_with_one_class"] = Math.round((1.0*num_with_one_class / num_samples) - (last_averaged_point.num_with_one_class));
                data["num_with_one_buddy"] = Math.round((1.0*num_with_one_buddy / num_samples) - (last_averaged_point.num_with_one_buddy));
                data["num_attended_one_event"] = Math.round((1.0*num_attended_one_event / num_samples) - (last_averaged_point.num_attended_one_event));
            } else {
                data["num_total_users"] = Math.round(num_total_users / num_samples);
                data["num_active_users"] = Math.round(num_active_users / num_samples);
                data["num_authenticated"] = Math.round(num_authenticated / num_samples);
                data["num_filled_in_profile"] = Math.round(num_filled_in_profile / num_samples);
                data["num_hit_home_page"] = Math.round(num_hit_home_page / num_samples);
                data["num_with_one_class"] = Math.round(num_with_one_class / num_samples);
                data["num_with_one_buddy"] = Math.round(num_with_one_buddy / num_samples);
                data["num_attended_one_event"] = Math.round(num_attended_one_event / num_samples);
            }
            if ($scope.sample_type == "funneled") {
                var orig = angular.copy(data);
                data["num_active_users"] = Math.round(100.0 * data["num_active_users"] / orig["num_total_users"]);
                data["num_authenticated"] = Math.round(100.0 * data["num_authenticated"] / orig["num_active_users"]);
                data["num_filled_in_profile"] = Math.round(100.0 * data["num_filled_in_profile"] / orig["num_authenticated"]);
                data["num_hit_home_page"] = Math.round(100.0 * data["num_hit_home_page"] / orig["num_filled_in_profile"]);
                data["num_with_one_class"] = Math.round(100.0 * data["num_with_one_class"] / orig["num_hit_home_page"]);
                data["num_with_one_buddy"] = Math.round(100.0 * data["num_with_one_buddy"] / orig["num_with_one_class"]);
                data["num_attended_one_event"] = Math.round(100.0 * data["num_attended_one_event"] / orig["num_with_one_buddy"]);
            }
            if ($scope.sample_type == "percentages") {
                var orig = angular.copy(data);
                data["num_active_users"] = Math.round(100.0 * data["num_active_users"] / orig["num_total_users"]);
                data["num_authenticated"] = Math.round(100.0 * data["num_authenticated"] / orig["num_total_users"]);
                data["num_filled_in_profile"] = Math.round(100.0 * data["num_filled_in_profile"] / orig["num_total_users"]);
                data["num_hit_home_page"] = Math.round(100.0 * data["num_hit_home_page"] / orig["num_total_users"]);
                data["num_with_one_class"] = Math.round(100.0 * data["num_with_one_class"] / orig["num_total_users"]);
                data["num_with_one_buddy"] = Math.round(100.0 * data["num_with_one_buddy"] / orig["num_total_users"]);
                data["num_attended_one_event"] = Math.round(100.0 * data["num_attended_one_event"] / orig["num_total_users"]);
            }
            return data;
        }

        var num_samples, num_total_users, num_active_users,
            num_authenticated, num_filled_in_profile, num_hit_home_page,
            num_with_one_class, num_with_one_buddy,
            num_attended_one_event, buddy_ratio;
        
        reset_aggregates();
        $scope.combined.reverse();
        var start_date = $scope.combined[0].display_date;
        var last_averaged_point = false;

        // Assumes combined has been created.
        for (var m_index in $scope.combined) {
            m = $scope.combined[m_index];

            if (m.type == "event" || m.type == "code_push") {
                buddy_ratio_to_save = Math.round(buddy_ratio / num_samples);
                if ($scope.sample_type == "percentages" && !$scope.aggregate) {
                    num_samples = num_samples / 100
                }
                if (num_samples > 0) {
                    data = make_data_point();
                    $scope.averaged.push(data);
                    last_averaged_point = {
                        "num_total_users": num_total_users / num_samples,
                        "num_active_users": num_active_users / num_samples,
                        "num_authenticated": num_authenticated / num_samples,
                        "num_filled_in_profile": num_filled_in_profile / num_samples,
                        "num_hit_home_page": num_hit_home_page / num_samples,
                        "num_with_one_class": num_with_one_class / num_samples,
                        "num_with_one_buddy": num_with_one_buddy / num_samples,
                        "num_attended_one_event": num_attended_one_event / num_samples,
                    };
                }
                $scope.averaged.push(m);
                reset_aggregates();
            } else {
                num_samples += 1;
                if ($scope.sample_type == "percentages" && !$scope.aggregate) {
                    num_total_users += 1.0 * m.num_total_users / 100;
                    num_active_users += 1.0 * m.num_active_users / 100;
                    num_authenticated += 1.0 * m.num_authenticated / 100;
                    num_filled_in_profile += 1.0 * m.num_filled_in_profile / 100;
                    num_hit_home_page += 1.0 * m.num_hit_home_page / 100;
                    num_with_one_class += 1.0 * m.num_with_one_class / 100;
                    num_with_one_buddy += 1.0 * m.num_with_one_buddy / 100;
                    num_attended_one_event += 1.0 * m.num_attended_one_event / 100;
                } else {
                    num_total_users += 1.0 * m.num_total_users;
                    num_active_users += 1.0 * m.num_active_users;
                    num_authenticated += 1.0 * m.num_authenticated;
                    num_filled_in_profile += 1.0 * m.num_filled_in_profile;
                    num_hit_home_page += 1.0 * m.num_hit_home_page;
                    num_with_one_class += 1.0 * m.num_with_one_class;
                    num_with_one_buddy += 1.0 * m.num_with_one_buddy;
                    num_attended_one_event += 1.0 * m.num_attended_one_event;
                }
                buddy_ratio += m.buddy_ratio;
            }
        }
        if (num_samples > 0) {
            $scope.averaged.push(make_data_point());
    
        }
        reset_aggregates();
        $scope.combined.reverse();
        $scope.averaged.sort(sort_events).reverse();
    }

    $scope.init_dashboard = function() {
        $scope.show_events = true;
        $scope.show_code_pushes = true;
        $scope.aggregate = true;
        $scope.sample_type = "funneled";

        $scope.message = 'Hello, world!';
        $scope.data_points = window.dashboardData.data_points;
        $scope.milestones = window.dashboardData.milestones;
        
        $scope.update_display_data();
    }
});