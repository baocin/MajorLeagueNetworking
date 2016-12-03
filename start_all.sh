#!/bin/bash
npm start .
python3 LanguageProcessingAPI/run.py
./LanguageProcessingAPI/stanford-corenlp-full-2016-10-31/start.sh
./LanguageProcessingAPI/SimpleNLG/start.sh
