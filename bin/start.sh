#!/bin/sh

# Запускаем FastAPI в фоновом режиме
echo "Starting FastAPI application..."
make start &

# Ждем немного, чтобы FastAPI успел запуститься
sleep 3

# Запускаем nginx на переднем плане
echo "Starting Nginx..."
nginx -g "daemon off;"