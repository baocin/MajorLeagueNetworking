var express = require('express');
//var favicon = require('serve-favicon');
var router = express.Router();
var twitter = require('twitter');
var request = require('request'); //For interfacing with REST apis

//API Keys
var api_keys = require('../api_keys.json')

//Setup Twitter api
var client = new twitter({
  consumer_key: api_keys.Twitter.CONSUMER_KEY,
  consumer_secret: api_keys.Twitter.CONSUMER_SECRET,
  access_token_key: api_keys.Twitter.ACCESS_TOKEN_KEY,
  access_token_secret: api_keys.Twitter.ACCESS_TOKEN_SECRET,
});

//API URL for python parsing
parserUrl = "http://localhost:5000"

//Main website
//Typical Example:    http://localhost:3000/
//Example with query: http://localhost:3000/?topic=sports
router.get('/', function(req, res) {
    var topicQuery = req.query.topic || "";   //if undefined set to ""

    if (topicQuery == ""){            //No '?topic=whatever' in url
      res.render('index');      //Return default index page
      return;                         //Stop executing this request
    }

    //Setup Twitter Parameters
    var params = {
        q: topicQuery + " filter:links",  //results must have links
        result_type: 'popular',      //sort by popularity
        count: '100',                //Return 100 results (Twitter's max is 100)
    }
    //Send GET request
    getTweets(params).then(function(tweets){
      var processedTweets = extractExpandedUrls(tweets);

      //Keys are tweet objects, values are a list of topic suggestions
      var tweetDictionary = {}

      cachedPromises = processedTweets.map(getTopicSuggestions)
      results = Promise.all(cachedPromises)
      results.then(function(allResults){
        //All tweets processed
        allResults.forEach(function(result, index){
          console.log("Done Processing Tweet ID:" + result['tweetId'])
          tweetDictionary[result.tweetId] = result.suggestionList
        })
      }).then(function(){
        //DEV: Make sure everthing looks alright
        console.log("Dictionary:")
        console.log(tweetDictionary)

        //Finally, Render the page
        res.render('index', {          //Render the index page
          topic: topicQuery,               //our search query ex. 'sports'
          tweetResults: tweets,            //the json of the tweets
          count: tweets.statuses.length,   //how many tweet results
          tweetDictionary: tweetDictionary,  //Dictionary<Tweet,List<string(suggestions)>>
        });
      })
    });
});

var getTweets = function(params){
  //DEV: Logging the parameters used
  console.log("Twitter Parameters: ", params);
  //TODO: Check rate limiting
  return new Promise(function (fulfill, reject){
    client.get('search/tweets', params, function(error, tweets, response){
      if (error) reject(error);
      else fulfill(tweets);
    });
  });
};

var extractExpandedUrls = function(tweets){
  //Get just the expanded urls
  tweetUrls = []
  for (tweetIndex in tweets.statuses){
    tweet = tweets.statuses[tweetIndex]
    for (urlIndex in tweet.entities.urls){
      url = tweet.entities.urls[urlIndex]
      //DEV: The article extractor doesn't work well with twitter itself'
      //TODO: Check how this works on more websites (make whitelist?)
      if (url.expanded_url.indexOf('twitter') !== -1){
        continue;
      }
      //Use tweet.text to return the tweet text as well
      tweetUrls.push({'tweetId': tweet.id, 'url': url.expanded_url});
    }
  }
  return tweetUrls;
}

var getTopicSuggestions = function(tweetWithUrl){
  var url = tweetWithUrl.url
  var tweetId = tweetWithUrl.tweetId
  console.log("Processing Topic Suggestions for url: " + url)
  return new Promise(function (fulfill, reject){
    request.get({ url: parserUrl + "/parse/facts", qs:{url : url}}, function(error, response, body){
      //console.log(error);
      //console.log(response);
      //console.log(body);
      if (!error && response.statusCode == 200){
        //If everything is okay
        //console.log(body);
        fulfill({'tweetId': tweetId, 'suggestionList': body });

      }else{
        reject(error + "" + response.statusCode)
      }
    })
  })
}

module.exports = router;
