#!/bin/bash
mvn clean install -DskipTests
sleep 1
mvn exec:java
