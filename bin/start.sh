#!/bin/sh

# Запускаем FastAPI в фоновом режиме
echo "Starting FastAPI application..."
make start &

# Ждем немного, чтобы FastAPI успел запуститься
while ! nc -z 127.0.0.1 8080; do
  sleep 1
done

# Запускаем nginx на переднем плане
echo "Starting Nginx..."
nginx -g "daemon off;"