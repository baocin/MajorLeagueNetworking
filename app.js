var express = require('express');
var favicon = require('serve-favicon');
var twitter = require('twitter');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var path = require('path');

//API Keys
var api_keys = require('./api_keys.json')
//Routing
var routes = require('./routes/index');

//Set up express js
var app = express();
//view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
//app.use(express.static(path.join(__dirname, 'public')));

//Routing for static assets
app.use('/static', express.static(__dirname + '/static'));

//routes
app.use('/', routes);

//Redirect favicon to static directory
app.use(favicon(__dirname + '/static/favicon.ico'));

//catch 404 and forward to error handler
app.use(function(req, res, next){
  var err = new Error('Sorry, Not Found');
  err.status = 404;
  next(err);
});

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

module.exports = app;
