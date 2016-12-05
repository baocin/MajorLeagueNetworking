#!/bin/bash
echo "Remember to move api_keys.json to the top of the git folder"
echo "Also download the standford models"

rm 'output-nodeui.log'
npm install && nodemon >> output-nodeui.log 2>>output-nodeui.log &
echo "Starting Node UI Server (status:" $? ")"

cd LanguageProcessingAPI/
rm 'output-extractor.log'
python3 run.py >> output-extractor.log 2>>output-nodeui.log &
echo "Starting Python Article Extractor Server (status:" $? ")"

cd stanford-corenlp-full-2016-10-31/
rm 'output-nlp.log'
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000 999999  > output-nlp.log 2>&1 & >> output-nlp.log 2>>output-nodeui.log &
echo "Starting Stanford Core NLP Server (status:" $? ")"

cd ../SimpleNLG/
rm 'output-nlg.log'
`bash mvn clean install -DskipTests && sleep 1 && mvn exec:java` >> output-nlg.log 2>>output-nodeui.log &
echo "Starting Sentence Generator Server (status:" $? ")"


sleep 3 && curl 'http://localhost:9000/?properties=%7B%22annotators%22%3A%20%22tokenize%2Cssplit%2Cpos%2Clemma%2Cner%2Cparse%2Cdepparse%2Copenie%2Ckbp%2Csentiment%22%2C%20%22date%22%3A%20%222016-12-04T15%3A05%3A46%22%7D&pipelineLanguage=en' -H 'Pragma: no-cache' -H 'Origin: http://localhost:9000' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0' -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: http://localhost:9000/' -H 'DNT: 1' --data 'sadasdsdf' --compressed &

echo "Press Enter to quit all servers"
read
killall node
killall java
killall python3
