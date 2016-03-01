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
name="The Little Drop"
fname="the-little-drop"
org="org.grimfang-studio"
orgFull="GrimFang Studio"
mail="info@grimfang-studio.org"
releasesDir=./releases
gameName=$releasesDir/Game$current_time.p3d
iconPath=./Design/Icons

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
pdeploy -n $fname -N "$name" -v $version -o $releasesDir -a $org -A "$orgFull" -e $mail -i $iconPath/Icon16.png -i $iconPath/Icon32.png -i $iconPath/Icon48.png -i $iconPath/Icon64.png -i $iconPath/Icon128.png -s $gameName installer

echo ""
echo "installers created"
echo "=============================="
