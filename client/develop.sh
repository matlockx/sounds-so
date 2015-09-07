#!/bin/sh
set -e

cd "$(dirname "$0")"

echo "removing old container"
docker rm -f sounds-so-client-dev || true

echo "building base container"
docker build -t sounds-so-client .

echo "starting development container"
docker run --name sounds-so-client-dev -d -p 9000:80 \
  -e BACKEND_HOST=95.138.174.122 \
  -v $PWD/src:/app/src:ro \
  -v $PWD/gulpTasks:/app/gulpTasks:ro \
  -v $PWD/index.html:/app/index.html:ro \
  sounds-so-client:latest

echo "Open http://localhost:9000 in your browser"

# jump into the container
docker exec -it sounds-so-client-dev bash

# stop development container again
docker rm -f sounds-so-client-dev
