#!/bin/bash
echo 'Welcome to the iot-patcher'
read -p 'Please, specify the path to your firmware file: ' path
echo 
read -p 'Please, specify the path to extracted data: ' extracted
echo
echo 'Starting binwalking on $path, extracted data will be in $extracted folder.'
binwalk --signature --term -e $path -C $extracted > $extracted/binwalk.log
