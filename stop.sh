path=`dirname $0`
kill `cat ${path}/logs/gunicorn.pid`