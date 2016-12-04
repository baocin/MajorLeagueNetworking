#!/bin/bash
mvn clean install -DskipTests
sleep 2
mvn exec:java
