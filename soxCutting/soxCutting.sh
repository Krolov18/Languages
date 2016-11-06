#!/usr/bin/env bash

FILE=$1

cat $FILE | while read line do
    x, y, z, t <<< $line
    sox $x $y trim $z $t