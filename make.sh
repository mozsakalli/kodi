#!/bin/sh

rm -rf plugin.video.hdfilmcehennemi.zip
find plugin.video.hdfilmcehennemi -name ".DS_Store" -depth -exec rm {} \;
zip -r plugin.video.hdfilmcehennemi.zip plugin.video.hdfilmcehennemi
