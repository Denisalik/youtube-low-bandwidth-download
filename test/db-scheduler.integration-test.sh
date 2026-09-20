#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <DB_CLEANUP_HOUR> <CLEANUP_MINUTE>" >&2
    exit 1
fi

DB_CLEANUP_HOUR="$1"
CLEANUP_MINUTE="$2"

docker rm -f sched-test 2>/dev/null || true

docker build -t yout-backend:latest .
docker run -d --name sched-test -e DB_CLEANUP_HOUR="${DB_CLEANUP_HOUR}" -e CLEANUP_MINUTE="${CLEANUP_MINUTE}" -p 8000:8000 -v ./data/files:/data/files -v ./data/sql:/data/sql yout-backend
docker exec sched-test date
      
sleep 3

curl -X POST http://localhost:8000/api/files -H 'Content-Type: application/json' -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "state": "deleted"}'
echo

curl -X GET http://localhost:8000/api/files
echo

sleep 30
curl -X GET http://localhost:8000/api/files
echo

docker stop sched-test
docker rm sched-test