#! /bin/sh
### BEGIN INIT INFO
# Provides:          blueberrypy
# Required-Start:    $remote_fs $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Set the CPU Frequency Scaling governor to "ondemand"
### END INIT INFO


PATH=~wk/bin:/sbin:/usr/sbin:/bin:/usr/bin
APP_PATH=~wk/private/kpi/4.1/pm/tc-informer.pp.ua
IF=0.0.0.0
PORT=7777

COMMAND="blueberrypy serve -b $IF:$PORT -d"

cd $APP_PATH

. $APP_PATH/env/bin/activate

$COMMAND

PID=`ps -o pid,args -A | grep "$COMMAND" | grep -v "grep" | tac | tail -n 1 | awk '{print $1}'`

echo $PID > $APP_PATH/lock.pid
