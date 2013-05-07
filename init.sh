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

COMMAND="blueberrypy serve -b $IF:$PORT -d -P $APP_PATH/lock.pid"

cd $APP_PATH

. $APP_PATH/env/bin/activate

$COMMAND
