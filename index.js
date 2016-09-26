var express = require('express');
var favicon = require('serve-favicon');
var twitter = require('twitter');

//Set up express js
var app = express();
app.set('view engine', 'ejs');

//Setup Twitter api
var client = new twitter({
  consumer_key: process.env.TWITTER_CONSUMER_KEY,
  consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
  access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
  access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET,
});

//Routing for static assets
app.use('/static', express.static(__dirname + '/static'));

//Redirect favicon to static directory
app.use(favicon(__dirname + '/static/favicon.ico'));

//Main website
//Typical Example:    http://localhost:3000/
//Example with query: http://localhost:3000/?topic=sports
app.use('/', function(req, res) {
    var topicQuery = req.query.topic || "";   //if undefined set to ""

    if (topicQuery == ""){            //No '?topic=whatever' in url
      res.render('pages/index');      //Return default index page
      return;                         //Stop executing this request
    }

    //Setup Twitter Parameters
    var params = {
        q: topicQuery + " filter:links",  //results must have links
        result_type: 'popular',      //sort by popularity
        count: '100',                //Return 100 results (Twitter's max is 100)
    }

    //DEV: Logging the parameters used
    console.log("Twitter Parameters: ", params);

    //TODO: Check rate limiting

    //Send GET request
    client.get('search/tweets', params, function(error, tweets, response) {
        // console.log(tweets); //DEV: Used to see the raw json returned by Twitter
        if (!error) {   //All is well
            res.render('pages/index', {          //Render the index page
                topic: topicQuery,               //our search query ex. 'sports'
                tweetResults: tweets,            //the json of the tweets
                count: tweets.statuses.length,   //how many tweet results
            });
        } else {
            console.log(error);       //Something went wrong, print to console
        }
    });
});

app.listen(3000, function() {
    console.log('Listening on port 3000.');
    console.log('URL: http://localhost:3000/');
    console.log('JSON URL: http://localhost:3000/?topic=sports');
});
