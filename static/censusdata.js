var app = angular.module('censusdata', [], function($interpolateProvider) {
    // Avoid conflict with Flask templates
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

app.controller('dataCtrl', function ($scope, $http) {
    $scope.selected_column = null;
    $scope.ignored_rows = 0;

    $scope.reload = function() {
        $http.get('/results?key=' + $scope.selected_column).success(function(data) {
            $scope.lines = data.results;
            $scope.ignored_rows = data.ignored_rows;
            $scope.ignored_values = data.ignored_values;
        });
    };
});