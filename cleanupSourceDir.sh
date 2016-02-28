#!/bin/sh
echo "removing pyc files"
find ./game/ -name '*.pyc' -delete
echo "removing pyo files"
find ./game/ -name '*.pyo' -delete
echo "removing ~ (backup) files"
find ./game/ -name '*.*~' -delete
