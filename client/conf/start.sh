#!/bin/sh

BACKEND_HOST=${BACKEND_HOST:-backend}
sed -i -e "s/BACKEND/${BACKEND_HOST}/g" /etc/nginx/sites-available/default
exec nginx
