const iconv = require('iconv-lite');
const spawn = require('child_process').spawn;
var exec = require('child_process').exec;
//
// // 成功的例子
// exec('ls', { encoding: 'utf8' }, function(error, stdout, stderr){
//     if(error) {
//         console.error('error: ' + error);
//         return;
//     }
//     console.log('stdout: ' + stdout);
//     console.log('stderr: ' + typeof stderr);
// });
//
// var child_process = require('child_process');
// var iconv = require('iconv-lite');
var encoding = 'cp936';
var binaryEncoding = 'binary';

exec('ls', {encoding: binaryEncoding}, function(err, stdout, stderr){
    if(err) {
      console.error('error: ' + iconv.decode(new Buffer(err, binaryEncoding), encoding));
      return;
    }
});
    //console.log(iconv.decode(new Buffer(stdout, binaryEncoding), encoding), iconv.decode(new Buffer(stderr, binaryEncoding), encoding));
