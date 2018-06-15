var express = require('express');
var bodyParser = require('body-parser');
// var process = require('child_process');
var app = express();
var util = require('util');
var exec = util.promisify(require('child_process').exec);
var cmd = 'code C:\Program Files';


app.use(bodyParser.urlencoded({ extended: false }));

//模拟处理命令
app.get('/', function(req, res) {
  // exec(cmd, function(err, stdout, stderr) {
  //   if (err) {
  //     console.log(err);
  //   } else {
  //     console.log(stdout);
  //   }
  // });
  console.log(__dirname);
  res.send('ok');
});

app.post('/handleFaces', function(req, res) {
  var data = req.body;
  console.log(data.name);
  res.send('ok');
});

app.listen(8007, function() {
  console.log('listening on 8007');
});
