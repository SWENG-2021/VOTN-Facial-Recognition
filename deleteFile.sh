#!/bin/sh
if [ -f "$1" ]; then
        echo "Deleting file $1"
        sudo rm "$1"
else
        echo "No such file exists"
fi
