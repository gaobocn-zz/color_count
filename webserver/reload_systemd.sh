#!/bin/bash

# run this after updating color_count.service

systemctl daemon-reload
systemctl restart color_count.service
