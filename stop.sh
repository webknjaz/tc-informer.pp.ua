#!/bin/sh

PATH=~wk/bin:/sbin:/usr/sbin:/bin:/usr/bin
APP_PATH=~wk/private/kpi/4.1/pm/tc-informer.pp.ua
IF=0.0.0.0
PORT=7777

COMMAND="blueberrypy serve -b $IF:$PORT -d"

cd $APP_PATH

kill `cat $APP_PATH/lock.pid`
