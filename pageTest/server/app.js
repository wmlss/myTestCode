var mongoose = require("mongoose");
mongoose.connect('mongodb://127.0.0.1:27017/test');
var express = require('express');
var ObjectID = require('mongodb').ObjectID;
var app = express();
var bodyParse = require('body-parser');
var testModel = require('./models/test');

app.get('/add', function(req, res) {
  var content = req.query.content;
  console.log(content);
  testModel.insertMany([{'content': content}], function(err) {
    if (err) {
      console.log(err);
    }
  });
  res.send(content);
});


app.get('/delete', function(req, res) {
  var id = req.query.id;
  console.log(new ObjectID(id));
  testModel.deleteOne({'_id': new ObjectID(id)}, function(err) {
    if (err) {
      console.log(err);
    }
  });
  res.send(id);
});


app.get('/find', function(req, res) {
  testModel.find({}).exec().then(function(response) {
    console.log(response);
    var result = {
      status: 200,
      data: response
    };
    res.send(result);
  });
});

app.listen(8080, function() {
  console.log('listening on 8080');
});
