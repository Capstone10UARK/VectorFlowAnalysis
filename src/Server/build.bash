#!/bin/sh
set -e

echo Compiling...
javac -cp ../../lib/java-json.jar *.java

echo Running...
java -cp ../../lib/java-json.jar:. CommandServer & py ../Client/main.py && fg


