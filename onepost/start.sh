uwsgi --ini /var/www/html/onepost/uwsgi.ini&&
tail -f /dev/null
exec "$@"
