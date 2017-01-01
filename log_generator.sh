#!/bin/bash

init() {
    NIFI_HOME=~/nifi-1.0.0
    KAFKA_HOME=~/kafka_2.11-0.10.1.0
}

start() {
    # Start NiFi
    echo "Starting NiFi.."
    sh "$NIFI_HOME"/bin/nifi.sh start
    NIFI_PID="$(pgrep -f RunNiFi)"
    echo "NiFi started, pid=$NIFI_PID"

    # Start Kafka
    echo "Starting Zookeeper"
    sh "$KAFKA_HOME"/bin/zookeeper-server-start.sh "$KAFKA_HOME"/config/zookeeper.properties &
    ZOOKEEPER_PID=$!
    echo "Zookeeper started, pid=$ZOOKEEPER_PID"

    sleep 10

    echo "Starting Kafka server"
    sh "$KAFKA_HOME"/bin/kafka-server-start.sh "$KAFKA_HOME"/config/server.properties &
    KAFKA_PID=$!
    echo "Kafka server started, pid=$KAFKA_PID"

    # Wait for a few seconds
    sleep 5

    # Start the log generator
    echo "Starting Locust.."
    locust -f src/nifi_client.py --host=http://localhost:8081 &
    LOCUST_PID=$!
    echo "Locust started, pid=$LOCUST_PID, http://localhost:8089"

    # Start the push server
    echo "Starting push server .."
    src/push_server.py &
    PUSH_SERVER_PID=$!
    echo "Push server started, pid=$PUSH_SERVER_PID, http://localhost:5000"

    # Start the UI
    echo "Starting dashboard .."
    ./dashboard.py &
    CLIENT_PID=$!
    echo "Dashboard UI started, pid=$CLIENT_PID, http://localhost:3000"

    echo "Done"
}

stop() {
    echo "Stopping Locust.."
    kill_process "locust"
    echo "Stopping push server.."
    kill_process "push_server"
    echo "Stopping the client (Dashboard UI).."
    kill_process "dashboard"
    echo "Stopping Kafka.."
    sh "$KAFKA_HOME"/bin/kafka-server-stop.sh
    echo "Kafka server stopped"
    sh "$KAFKA_HOME"/bin/zookeeper-server-stop.sh
    echo "Zookeeper stopped"
    return 0
}

kill_process() {
    PID="$(pgrep -f $1)"
    if  [[ "$PID" ]]
    then
        if ps -p $PID > /dev/null
        then
            echo "$PID is running, stopping it.."
            kill -9 $PID
        fi
    fi
}


main() {
    init
    "$@"
}

case "$1" in
    start|stop)
        main "$@"
        ;;
    restart)
        init
        stop
        start
        ;;
    *)
        echo "Usage start|stop|restart"
        ;;
esac