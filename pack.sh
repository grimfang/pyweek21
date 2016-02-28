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

current_time=$(date "+%Y%m%d-%H%M%S")
version=$(date "+%y.%m")
name="The Games name"
fname="the-game-name"
org="org.grimfang-studio"
orgFull="GrimFang Studio"
mail="info@grimfang-studio.org"
releasesDir=./releases
gameName=$releasesDir/Game$current_time.p3d
iconPath=./Design/icons

echo "=============================="
echo ""
echo "packing game: " $gameName
echo ""
packp3d -d game/ -r openal -x pdf -n x11 -n pdf -n mo -o $gameName
echo ""
echo "game packed"
echo "=============================="

echo "=============================="
echo ""
echo "Building installers in: " $releasesDir
echo ""

#
# self containing installer
#
pdeploy -n $fname -N "$name" -v $version -o $releasesDir -a $org -A "$orgFull" -e $mail -s $gameName installer

echo ""
echo "installers created"
echo "=============================="
