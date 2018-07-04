var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var testSchema = new Schema({
  content: {
    type: 'String'
  }
});

var testModule = mongoose.model('testCollection', testSchema);

module.exports = testModule;
