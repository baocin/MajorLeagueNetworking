#!/usr/bin/env bash
#
# Runs Stanford CoreNLP API Server

OS=`uname`
# Some machines (older OS X, BSD, Windows environments) don't support readlink -e
if hash readlink 2>/dev/null; then
  scriptdir=`dirname $0`
else
  scriptpath=$(readlink -e "$0") || scriptpath=$0
  scriptdir=$(dirname "$scriptpath")
fi


echo "java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 999999"
echo "If you get a out of memory error up -mx5g to -mx8g"
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 999999
sleep(5)
echo "Now running test execution (to preload language models)"
wget --post-data 'The quick brown fox jumped over the lazy dog.' 
'localhost:9000/?properties={"annotators":"tokenize,ssplit,pos","outputFormat":"json"}' -O -
