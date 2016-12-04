#!/bin/bash
echo "Remember to move api_keys.json to the top of the git folder"
echo "Also download the standford models"

`npm install && npm start` > /dev/null 2>&1 &

cd LanguageProcessingAPI/
echo `pwd`
python3 run.py > /dev/null 2>&1 &

cd stanford-corenlp-full-2016-10-31/
echo `pwd`
./start.sh > /dev/null 2>&1 &

cd ../SimpleNLG/
echo `pwd`
`bash start.sh` > /dev/null 2>&1 &


echo "Press Enter to quit all servers"
read
killall node
killall java
killall python3
