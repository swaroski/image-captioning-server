#!/bin/sh

# Start Nginx in foreground
nginx &

# Start Gunicorn in foreground
gunicorn -w 8 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
