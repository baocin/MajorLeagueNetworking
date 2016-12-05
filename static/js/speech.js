var pos = require('pos');
var persistSpeechAfterQuery;    //If the previous page was submitted via voice, auto restart voice recognition on the results page
var lastNounList = [];          //Store a list of nouns from the previous recognition
var speechEnabled = false;      //Voice recognition is disabled by default
var autoSubmit = true;          //Auto query heard proper nouns (like names)
var recognition;                //The recognition engine used to detect proper nouns
var supported = false;

$(document).ready(function(){
    //Need to wait for document to be done loading before finding elements
    persistSpeechAfterQuery = document.getElementById("persist-speech");

    //Check for voice recognition support in the browser
    if (!('webkitSpeechRecognition' in window)) {
        console.log("Your browser does not support webkitSpeechRecognition");
        $.notify("Your browser doesn't support Speech Recognition", { className: 'info', position:"bottom right" });
        supported = false;
    } else {
        $.notify("Your browser supports Speech Recognition. Give it a go!", { className: 'success', position:"bottom right" });
        supported = true;

        //Load the speech recognition engine
        setupSpeech();

        if (persistSpeechAfterQuery.value == 1){
            toggleSpeech();
        }
    }
});

function toggleSpeech(){
    if (!supported){
        speechEnabled = false;
        persistSpeechAfterQuery.value = 0;
        autoSubmit = false;
        return;
    }
    
    if (speechEnabled){
        $.notify("Speech Recognition stopped", { className: 'info', position:"bottom right" });
        persistSpeechAfterQuery.value = 0;
        stopSpeech()
    }else{
        $.notify("Speech Recognition started - say a player or team name", { className: 'info', position:"bottom right" });
        persistSpeechAfterQuery.value = 1;
        startSpeech()
    }
    speechEnabled = !speechEnabled;
}

function startListening(){
    speechEnabled = true;
    refreshSpeech();
    setInterval(refreshSpeech, 30000);
}

function stopListening(){
    speechEnabled = false;
    stopSpeech();
}

function refreshSpeech(){
    stopSpeech()
    if (speechEnabled = true){
        startSpeech()
    }
}

function stopSpeech(){
    recognition.stop()
    return;
}

function startSpeech(){
    setupSpeech();
    recognition.start();
}

function setupSpeech(){
    recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = function() { 
        
        console.log("Speech recognition started")
    }

    recognition.onresult = function(event) {
        final_transcript = ""
        transcript = ""
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
                newNounList = []

                //Add a non-noun to the end of the transcript so that the word parser will find proper names at the end of the original transcript
                final_transcript += " blank"

                var words = new pos.Lexer().lex(final_transcript);
                var tagger = new pos.Tagger();
                var taggedWords = tagger.tag(words);
                
                
                var temporaryNoun = ""; //For two word long nouns ("Cam Newton") 
                for (i in taggedWords) {
                    var taggedWord = taggedWords[i];
                    var word = taggedWord[0];
                    var tag = taggedWord[1];
                    console.log(word + " /" + tag);
                    if (tag == "NNP" || tag == "NNPS"){
                        temporaryNoun += " " + word;
                    }else{
                        if (temporaryNoun.length > 0){
                            newNounList.push(temporaryNoun);
                            temporaryNoun = "";
                        }
                    }
                }
                console.log("Last Noun List: " + lastNounList)
                console.log("New Noun List: " + newNounList)
                lastNounList = newNounList;

                //Auto submit the query
                if (autoSubmit && lastNounList.length > 0){
                    persistSpeechAfterQuery.value = 1;
                    submitQuery(lastNounList.join(' '))
                }
            }
        }
        
        console.log("final: " + final_transcript)

        //console.log("transcript: " + transcript )
    }
    recognition.onerror = function(event) { 
        console.log("Something bad happened during speech recognition.")
        }
    recognition.onend = function() { 
        console.log("Speech recognition ended")
    }
}

function submitQuery(text){
    stopListening();    //Prevent a new query from accidentally being 

    var searchForm = document.getElementById('form');
    var searchBox = document.getElementById('query');
    searchBox.value = lastNounList.join(' ');
    searchForm.submit();


}