#!/bin/sh

rm -rf ~/Library/Application\ Support/Kodi/addons/plugin.video.hdfilmcehennemi
find plugin.video.hdfilmcehennemi -name ".DS_Store" -depth -exec rm {} \;
zip -r plugin.video.hdfilmcehennemi.zip plugin.video.hdfilmcehennemi
