function SubscriberService(http) {
    var me = this;

    me.serverUrl = 'http://localhost:5000';
    me.sse = null;

    me.register = function() {
        return http.get(me.serverUrl + '/register');
    };

    me.unsubscribe = function(subscriberId) {
        http.get(me.serverUrl + '/unsubscribe/' + subscriberId + '/proxy_logs')
            .then(
                    function(response) {
                        console.log('Going to close the subscription');
                        if (me.sse) {
                            me.sse.close();
                            console.log('Subscription closed.');
                        }
                    }
                );
    };

    me.subscribe = function(subscriberId, callback) {
        var source = new EventSource(me.serverUrl + '/subscribe/' + subscriberId + '/proxy_logs');
        source.addEventListener('message', callback, false);
        source.addEventListener('open', function(e) {
            console.log('Opening a new connection');
        }, false);
        source.addEventListener('error', function(e) {
            console.log('There was an error!');
            if (e.readyState == EventSource.CLOSED) {
                console.log('Server closed the connection! Terminating..');
                source.close();
            }
        }, false);
        me.sse = source;
        console.log('Successfully subscribed');
    };
}
