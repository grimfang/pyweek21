#!/bin/sh

version=$(date "+%y.%m")
name="The Little Drop"
fname="the-little-drop"
org="org.grimfang-studio"
orgFull="GrimFang Studio"
mail="info@grimfang-studio.org"
releasesDir=./releases
gameName=$releasesDir/LittleDrop.p3d
iconPath=./Design/Icons

echo "=============================="
echo ""
echo "Building installers in: " $releasesDir
echo ""

#
# self containing installer
#
#pdeploy -n $fname -N "$name" -v $version -o $releasesDir -a $org -A "$orgFull" -e $mail -i $iconPath/Icon16.png -i $iconPath/Icon32.png -i $iconPath/Icon48.png -i $iconPath/Icon64.png -i $iconPath/Icon128.png -s $gameName installer
echo "::: CREATING LINUX INSTALLERS :::"
pdeploy -P linux_i386 -P linux_amd64 -n $fname -N "$name" -v $version -o $releasesDir -a $org -A "$orgFull" -e $mail -i $iconPath/Icon16.png -i $iconPath/Icon32.png -i $iconPath/Icon48.png -i $iconPath/Icon64.png -i $iconPath/Icon128.png -s $gameName installer
echo "::: CREATING WINDOWS INSTALLERS :::"
pdeploy -P win_i386 -P win_amd64 -n $fname -N "$name" -v $version -o $releasesDir -a $org -A "$orgFull" -e $mail -i $iconPath/Icon16.png -i $iconPath/Icon32.png -i $iconPath/Icon48.png -i $iconPath/Icon64.png -i $iconPath/Icon128.png -s $gameName installer
echo "::: CREATING OSX INSTALLERS :::"
pdeploy -P osx_i386 -P osx_amd64 -n $fname -N "$name" -v $version -o $releasesDir -a $org -A "$orgFull" -e $mail -i $iconPath/Icon16.png -i $iconPath/Icon32.png -i $iconPath/Icon48.png -i $iconPath/Icon64.png -i $iconPath/Icon128.png -s $gameName installer

echo ""
echo "installers created"
echo "=============================="
