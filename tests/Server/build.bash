#!/bin/sh
set -e

echo Compiling...
javac -cp ../lib/java-json.jar TestCommandServer.java

echo Running...
java -cp .:../lib/java-json.jar TestCommandServer

