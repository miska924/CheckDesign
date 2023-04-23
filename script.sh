#!/bin/bash

cd ~/CheckDesign
while [ 1 -le 1 ]; do

    git pull

    sudo mv srs/* -r var/www/html/

    docker build . -t check-design:1.0

    docker run check-design:1.0 --token=$TOKEN

done