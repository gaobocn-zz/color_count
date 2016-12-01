#!/bin/bash


gunicorn --workers 3 --bind 0.0.0.0:8000 --forwarded-allow-ips=* -m 007 --log-level debug --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log wsgi:app
