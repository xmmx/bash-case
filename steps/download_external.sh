#!/usr/bin/env bash

########################################################################################################################
#
# Define functions for Travis Build Script
#
########################################################################################################################

function download_fonts(){
    echo "--"
    echo Download fonts
    echo "--"

    Run "git clone --depth 1 git@github.com:$ORG/fonts.git ../out/fonts"
    Run "rm -rf fonts"
    Run "mv ../out/fonts/dist ./fonts"

    Run "zip -q -r fonts-${VERSION}.zip fonts"
    echo
}

function download_resources(){
    Run "cd dist"

    download_fonts
    
    Run "cd .."
    echo
}
