#!/bin/bash

cd ~/CheckDesign
while [ 1 -le 1 ]; do

    git pull

    docker build . -t check-design:1.0

    docker run check-design:1.0 --token=$TOKEN

done