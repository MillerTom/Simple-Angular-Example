describe('Angular Test', function(){
  beforeEach(module('GIT'));
  describe('Scope Check', function(){
    it('should check scopes.', inject(function($controller){
      var scope = {},
      ctrl =$controller('Repos', { $scope: scope });
      expect(scope.button).toBe("Fetch Repos");
      expect(scope.button2).toBe("Fetch User Info");
      expect(scope.formData).toBeDefined();
    }));
  });
  describe('Ajax Request', function(){
    var $httpBackend, $rootScope, createController;

    beforeEach(inject(function($injector) {
      // Set up the mock http service responses
      $httpBackend = $injector.get('$httpBackend');
      $rootScope = $injector.get('$rootScope');
      var $controller = $injector.get('$controller');

      createController = function() {
        return $controller('Repos', {'$scope' : $rootScope });
      };
    }));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      $httpBackend.verifyNoOutstandingRequest();
      $rootScope.formData = {};
    });


    it('should fetch user info.', function() {
      var controller = createController();

      $rootScope.formData = {'username': 'millertom'};
      $httpBackend.expectPOST('http://localhost:6543/user', $rootScope.formData).respond(200, {});
      $rootScope.user();
      expect($rootScope.button2).toBe('Fetching..');
      expect($rootScope.message2).toBe('');
      $httpBackend.flush();
      expect($rootScope.button2).toBe('Fetch User Info');
      expect($rootScope.message2).toBe('User Info');
      expect($rootScope.results2).toBeDefined();
    });

    it('should fetch user repos.', function() {
      var controller = createController();

      $rootScope.formData = {'username': 'millertom'};
      $httpBackend.expectPOST('http://localhost:6543/', $rootScope.formData).respond(200, {});
      $rootScope.submit();
      expect($rootScope.button).toBe('Fetching..');
      expect($rootScope.message).toBe('');
      $httpBackend.flush();
      expect($rootScope.button).toBe('Fetch Repos');
      expect($rootScope.message).toBe('Repo List');
      expect($rootScope.results).toBeDefined();
    })

  });
});