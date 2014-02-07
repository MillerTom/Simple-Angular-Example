var app = angular.module('GIT',[]);
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});



app.controller('Repos', function($scope, $http){
  $scope.button = 'Fetch Repos';
  $scope.button2 = 'Fetch User Info';
  $scope.formData = {};

  $scope.submit = function(){
    $scope.button = "Fetching..";
    $scope.message = '';
    $scope.results = [];
    $http.post('http://localhost:6543/', this.formData).success(function(response){
      if (response.length === 0){
        $scope.message = 'Failed';
      } else {
        $scope.message = 'Repo List';
      }
      $scope.button = "Fetch Repos";
      $scope.results = response;
    }).error(function(err){
      $scope.message = 'Failed';
      $scope.results = err;
    })
  };

  $scope.user = function(){
    $scope.button2 = "Fetching..";
    $scope.message2 = '';
    $scope.results2 = [];
    $http.post('http://localhost:6543/user', this.formData).success(function(response){
      if (response.length === 0){
        $scope.message2 = 'Failed';
      } else {
        $scope.message2 = 'User Info';
      }
      $scope.button2 = "Fetch User Info";
      $scope.results2 = response;
    }).error(function(err){
      $scope.message2 = 'Failed';
      $scope.results2 = err;
    })
  };
  $scope.change = function(){
    setTimeout(function(){
      $scope.user();
      $scope.submit();
    }, 1500);

  };
});