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

    # Start
    echo "Starting Locust.."
    locust -f src/nifi_client.py &
    LOCUST_PID=$!
    echo "Locust started, pid=$LOCUST_PID, http://localhost:8089"

    echo "Done"
}

stop() {
    echo "Stopping Kafka.."
    sh "$KAFKA_HOME"/bin/kafka-server-stop.sh
    echo "Kafka server stopped"
    sh "$KAFKA_HOME"/bin/zookeeper-server-stop.sh
    echo "Zookeeper stopped"

    LOCUST_PID="$(pgrep -f locust)"
    if  [[ "$LOCUST_PID" ]]
    then
        if ps -p $LOCUST_PID > /dev/null
        then
            echo "$LOCUST_PID is running, stopping it.."
            kill -9 $LOCUST_PID
        fi
    fi
    return 0
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