var express = require('express');
var app = express();

app.use('/page', express.static('./public'));

app.get('/', function(req, res) {
  var data = {
    msg: 'from server'
  };
  res.send(data);
});

app.listen(8080, function() {
  console.log('listening on 8080');
});
