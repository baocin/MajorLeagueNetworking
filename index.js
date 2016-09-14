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

//The main app
app.use('/', function (req, res) {
	res.render('pages/index');
});

app.listen(3000, function() {
	console.log('listening on port 3000');
});
