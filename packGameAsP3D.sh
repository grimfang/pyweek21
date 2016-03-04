#!/bin/sh

echo "=============================="
echo ""
echo "source directory cleanup"
echo ""
echo "removing pyc files"
find ./game/ -name '*.pyc' -delete
echo "removing pyo files"
find ./game/ -name '*.pyo' -delete
echo "removing ~ (backup) files"
find ./game/ -name '*.*~' -delete
echo ""
echo "source directory cleanup finished"
echo "=============================="

echo "=============================="
echo ""
gameName=./releases/LittleDrop.p3d
echo "packing game: " $gameName
echo ""
packp3d -d game/ -r openal -x pdf -n x11 -n pdf -n mo -o $gameName
echo ""
echo "game packed"
echo "=============================="
