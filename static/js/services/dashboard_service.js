function DashboardService() {
    var me = this;
    
    // Successful Response Trend
    me.successfulResponseTrendData = {
        successCount: 0,
        errorCount: 0
    };
    me.successfulResponseTrendGraphData = [];

    // Success vs Error Breakdown
    me.statusCodeData = [];
    me.statusCodeGraphData = [{ values: [], key: 'HTTP Status Codes'}]

    // Visit Summary: new visitors vs registered users
    me.visitSummaryData = {
        visitorCount: 0,
        userCount: 0
    };
    me.visitSummaryGraphData = [
        {
            label: 'New Visitors',
            value: 0
         },
         {
            label: 'Existing Users',
            value: 0
         }
    ];
    
    me.getSuccessfulResponseTrendGraphData = function() {
        return me.successfulResponseTrendGraphData;
    };
    
    me.getStatusCodeGraphData = function() {
        return me.statusCodeGraphData;
    };

    me.getVisitSummaryGraphData = function() {
        return me.visitSummaryGraphData;
    }    

    me.init = function() {
        me.successfulResponseTrendData.successCount = 0;
        me.successfulResponseTrendData.errorCount = 0;
    };

    me.updateSuccessfulResponseTrendGraphData = function() {
        var total = me.successfulResponseTrendData.successCount + me.successfulResponseTrendData.errorCount;
        var successRatio = (total === 0) ? 0 : me.successfulResponseTrendData.successCount / total;
        me.successfulResponseTrendGraphData.push({x: +new Date(), y: successRatio});
    };

    me.updateVisitSummaryGraphData = function() {
        me.visitSummaryGraphData[0].value = me.visitSummaryData.userCount;
        me.visitSummaryGraphData[1].value = me.visitSummaryData.visitorCount;
    };

    me.updateStatusCodeGraphData = function(statusCode) {
        var label = statusCode + '';
        isNew = true;

        for (var i = 0; i < me.statusCodeData.length; i++) {
            var item = me.statusCodeData[i];
            if (item.label === label) {
                item.value += 1;
                isNew = false;
                break;
            }
        }
        if (isNew) {
            me.statusCodeData.push({label: label, value: 1});
        }
        me.statusCodeData = me.statusCodeData.sort(function(a, b) {
            if (a.value < b.value) {
                return 1;
            }
            else if (a.value > b.value) {
                return -1;
            }
            else {
                return 0;
            }
        });
        me.statusCodeGraphData[0].values = me.statusCodeData;
    };

    me.parseMessage = function(msg) {

        // The captured HTTP response
        var data = JSON.parse(msg.data);

        // Successes vs errors
        if (data.res_status === 200) {
            me.successfulResponseTrendData.successCount++;
        } else {
            me.successfulResponseTrendData.errorCount++;
        }

        // Existing users vs new visitors
        if (data.authenticated === '-') {
            me.visitSummaryData.userCount++;
        } else {
            me.visitSummaryData.visitorCount++;
        }

        // Update visualisations
        me.updateSuccessfulResponseTrendGraphData();
        me.updateVisitSummaryGraphData();
        me.updateStatusCodeGraphData(data.res_status);
    };
}