echo off
title VFI Imaging
javac -cp ../../lib/java-json.jar *.java
start /b cmd /c java -cp ../../lib/java-json.jar;. CommandServer
python ../Client/main.py