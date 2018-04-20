echo off
title VFI Imaging
javac -cp ../../lib/java-json.jar *.java
start /b cmd /k java -cp ../../lib/java-json.jar;. CommandServer
python34 ../Client/main.py