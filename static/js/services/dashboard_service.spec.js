describe('Dashboard Service Factory', function() {
    var dashboardService;

    // Load the service module before each test
    beforeEach(angular.mock.module('app'));

    // Before each test, let the factory use the test object
    beforeEach(inject(function(_dashboardService_) {
        dashboardService = _dashboardService_;
    }));

    // Verify the factory does provide an instance
    it('should exist', function() {
        expect(dashboardService).toBeDefined();
        expect(dashboardService).not.toBeNull();
    });

    describe('.init()', function() {
        it('should exist', function() {
            expect(dashboardService.init).toBeDefined();
        });
    });

    describe('.getSuccessfulResponseTrendGraphData()', function() {
        it('should exist', function() {
            expect(dashboardService.getSuccessfulResponseTrendGraphData).toBeDefined();
        });

        it('should return the expected default data', function() {
            expect(dashboardService.getSuccessfulResponseTrendGraphData())
            .toEqual(dashboardService.successfulResponseTrendGraphData);
        });
    });

    describe('.getStatusCodeGraphData()', function() {
        it('should exist', function() {
            expect(dashboardService.getStatusCodeGraphData).toBeDefined();
        });

        it('should return the expected default data', function() {
            expect(dashboardService.getStatusCodeGraphData())
            .toEqual(dashboardService.statusCodeGraphData);
        });
    });

    describe('.getVisitSummaryGraphData()', function() {
        it('should exist', function() {
            expect(dashboardService.getVisitSummaryGraphData).toBeDefined();
        });

        it('should return the expected default data', function() {
            expect(dashboardService.getVisitSummaryGraphData())
            .toEqual(dashboardService.visitSummaryGraphData);
        });
    });

    describe('.updateSuccessfulResponseTrendGraphData()', function() {
        it('should exist', function() {
            expect(dashboardService.updateSuccessfulResponseTrendGraphData).toBeDefined();
        });
    });

    describe('.updateVisitSummaryGraphData()', function() {
        it('should exist', function() {
            expect(dashboardService.updateVisitSummaryGraphData).toBeDefined();
        });
    });

    describe('.updateStatusCodeGraphData()', function() {
        it('should exist', function() {
            expect(dashboardService.updateStatusCodeGraphData).toBeDefined();
        });
    });

    describe('.parseMessage()', function() {
        it('should exist', function() {
            expect(dashboardService.parseMessage).toBeDefined();
        });
    });

});