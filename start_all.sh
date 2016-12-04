#!/bin/bash
echo "Remember to move api_keys.json to the top of the git folder"
echo "Also download the standford models"

rm 'output-nodeui.log'
npm install && nodemon > output-nodeui.log  2>&1 &
echo "Starting Node UI Server (status:" $? ")"

cd LanguageProcessingAPI/
rm 'output-extractor.log'
python3 run.py > output-extractor.log 2>&1 &
echo "Starting Python Article Extractor Server (status:" $? ")"

cd stanford-corenlp-full-2016-10-31/
rm 'output-nlp.log'
`bash start.sh`  > output-nlp.log 2>&1 &
echo "Starting Stanford Core NLP Server (status:" $? ")"

cd ../SimpleNLG/
rm 'output-nlg.log'
`bash start.sh`   > output-nlg.log 2>&1 &
echo "Starting Sentence Generator Server (status:" $? ")"




echo "Press Enter to quit all servers"
read
killall node
killall java
killall python3
