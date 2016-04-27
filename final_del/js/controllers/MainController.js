/**
 * Created by MichaelYuja on 4/27/16.
 */
form.controller('MainController',  function($scope, $http) {
    $scope.timeSpan = 0;
    $scope.ecps = [{'email':'','calendar':''}];
    $scope.times = {};
    $scope.submit = function() {
        ecps = [];
        for (var i = 0; i < $scope.ecps.length; i++){
            if ($scope.ecps[i].email != '' && $scope.ecps[i].calendar != '') {
                ecps.push($scope.ecps[i])
            }
        }
        var req = {
            method: 'POST',
            url: 'http://ec2-54-174-75-62.compute-1.amazonaws.com/api/meetingTime',
            data: {
                timeSpan: $scope.timeSpan,
                calendars: ecps
            }
        };
        console.log("Submit was hit");
        console.log(req.data);
        $http(req).then(function(resp){
            $scope.times = resp.data
        });
    };

    //UI functions
    $scope.numUser = 1;
    $scope.showMinusButton = false;
    $scope.addEcps = function() {
        $scope.ecps.push({'email':'','calendar':''})
        $scope.numUser += 1;
    };
    $scope.subtractEcps = function() {
        if ($scope.numUser > 1) {
            $scope.ecps.pop();
            $scope.numUser -= 1;
        }
    };
    $scope.showMinus = function() {
        if ($scope.numUser > 1) {
            $scope.showMinusButton = true;
        }
        else {
            $scope.showMinusButton = false;
        }
    }
});