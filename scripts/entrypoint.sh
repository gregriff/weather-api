#!/bin/sh

python -m uvicorn api.main:app \
	--host=${HOST} \
	--port=${PORT} \
	--workers 1 \
	--log-level debug;
