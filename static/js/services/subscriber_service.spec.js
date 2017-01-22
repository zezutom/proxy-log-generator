describe('Subscriber Service', function() {
    var subscriberService;

    // Load the service module before each test
    beforeEach(angular.mock.module('app'));

    // Before each test, let the factory use the test object
    beforeEach(inject(function(_subscriberService_) {
        subscriberService = _subscriberService_;
    }));

    // Verify the factory does provide an instance
    it('should exist', function() {
        expect(subscriberService).toBeDefined();
        expect(subscriberService).not.toBeNull();
    });
});