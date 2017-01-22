function AppService() {
    var me = this;

    me.calculateRatio = function(a, b) {
        var total = a + b;
        ratio = (total === 0) ? 0 : a / total;
        return {x: +new Date(), y: ratio}
    };

    me.isSuccess = function(msg) {
        var data = JSON.parse(msg.data);
        return data.res_status === 200;
    };

    me.isAuthenticated = function(msg) {
        var data = JSON.parse(msg.data);
        return data.authenticated === '-';
    };

    me.updateStatusCodes = function(msg, statusCodes) {
        var data = JSON.parse(msg.data);
        var label = data.res_status + '';
        isNew = true;

        for (var i = 0; i < statusCodes.length; i++) {
            var statusCode = statusCodes[i];
            if (statusCode.label === label) {
                statusCode.value += 1;
                isNew = false;
                break;
            }
        }
        if (isNew) {
            statusCodes.push({label: label, value: 1});
        }
        return statusCodes.sort(function(a, b) {
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
    };
}