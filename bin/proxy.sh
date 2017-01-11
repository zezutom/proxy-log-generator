#!/usr/bin/env bash

# Resolve conf and source paths
CWD="$(dirname "$0")"
CONF_DIR="$CWD/../conf"
SRC_DIR="$CWD/../src/main"

# Read app config
source "$CWD/read_ini.sh"
read_ini "$CWD/../conf/app.ini"

start() {
    echo "Starting Locust.."
    echo "$SRC_DIR/locust_client.py"
    locust -f "$SRC_DIR/locust_client.py" --host="${INI__Locust__host}" --port="${INI__Locust__port}" &

    # Start the push server
    echo "Starting push server .."
    "$SRC_DIR/push_server.py" &

    echo "Starting web app .."
    "$SRC_DIR/app.py" &
}

stop() {
    echo "Stopping Locust.."
    kill_process "locust"

    echo "Stopping push server.."
    kill_process "push_server.py"

    echo "Stopping web app.."
    kill_process "app.py"
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

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage start | stop | restart"
        ;;
esac