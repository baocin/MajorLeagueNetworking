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


echo "java -mx5g -cp \"*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 999999"
echo "If you get a out of memory error up -mx5g to -mx8g"
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 999999 


sleep 5
echo "Caching NLP models..."
curl 'http://localhost:9000/?properties=%7B%22annotators%22%3A%20%22tokenize%2Cssplit%2Cpos%2Clemma%2Cner%2Cparse%2Cdepparse%2Copenie%2Ckbp%2Csentiment%22%2C%20%22date%22%3A%20%222016-12-04T15%3A05%3A46%22%7D&pipelineLanguage=en' -H 'Pragma: no-cache' -H 'Origin: http://localhost:9000' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0' -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: http://localhost:9000/' -H 'DNT: 1' --data 'sadasdsdf' --compressed
