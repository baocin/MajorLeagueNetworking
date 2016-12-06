# MajorLeagueNetworking
Group 18 - BOLT - Senior Software Project

Team Members: Serge Neri, Mosuela Joanne, Darshesh Patel, Michael Pedersen, Shilpa Arora

# Goal
Major Leage Networking (MLN) is a small talk aid that helps users immediately engage in conversation about sports.
Users query MLN in realtime for any sports topic and receive the most relevant talking points for use in small talk interactions.
MLN empowers a user's social life, breaking the ice with co-workers and new acquaintances.

# How to install
1. Open a terminal
2. Clone this repo
    > git clone https://github.com/baocin/MajorLeagueNetworking.git
3. Navigate into the cloned directory
    > cd MajorLeagueNetworking
4. Copy the "api_keys.json" file into this directory. It should look something like this:
    ~~~~ 
    {
       "Twitter":
        {
            "CONSUMER_KEY": "XXXXXXXXXXXXXXXXXXX",
            "CONSUMER_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "ACCESS_TOKEN_KEY": "XXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "ACCESS_TOKEN_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        }
    }
    ~~~~ 

5. Copy the "stanford-corenlp-3.7.0-models.jar" file to the "LanguageProcessingAPI/stanford-corenlp-full-2016-10-31/" folder
6. This command starts up all FOUR servers. The servers consume ports 3000,5000,9000, and 9090. To quit them all press enter.
    > ./start_all.sh

7. Open your favorite browser (Chrome) to http://localhost:3000
8. Use the website!
9. ...
10. Profit?


# Technologies Used: 
- Node.js: UI/Presentation Layer
    - [webkitSpeechRecognition](https://dvcs.w3.org/hg/speech-api/raw-file/tip/speechapi.html): Client-side 
    - [pos](https://www.npmjs.com/package/pos): Client-side word classification into Noun, Verb, etc. 
    - [Bootstrap](http://getbootstrap.com/): Making everything look pretty
        - JQuery: Prebundled
    - [Notify.js](https://notifyjs.com/): Little alerts about voice recognition status
    - [Browserify](http://browserify.org/): To require() npm libraries client-side
    - [request](https://www.npmjs.com/package/request): Make REST API calls a whole lot easier
    - [express.js](http://expressjs.com/): Simple routing and http server
    - [twitter](https://www.npmjs.com/package/twitter): Needed inorder to interact with Twitter API
    - [EJS](https://www.npmjs.com/package/ejs): HTML Templating

- Python: News Article Extraction Service
    - [newspaper](http://newspaper.readthedocs.io/): Extract just the text out of a news article
    - [Flask](http://flask.pocoo.org/): Used to expose a REST API to other components of the system
    - [requests](http://docs.python-requests.org/en/master/): Made calling REST APIs well

- Java: [Standford CoreNLP Server](http://stanfordnlp.github.io/CoreNLP/corenlp-server.html)
    - Used to extract subject-relation-object triples from news article text

- Java: [SimpleNLG Service](https://github.com/simplenlg/simplenlg)
    - For generating sentences from extracted "fact" triples