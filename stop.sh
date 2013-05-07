#!/bin/sh

APP_PATH=~wk/private/kpi/4.1/pm/tc-informer.pp.ua
kill `cat $APP_PATH/lock.pid`
