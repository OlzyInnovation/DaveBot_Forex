const mongoose = require('mongoose');

const DataSchema = new mongoose.Schema({
  DataConfig: [
    {
      _id: String,
      url: String,
      token: String,
      status: String,
      track: String,
    },
  ],
});

module.exports = mongoose.model('Data', DataSchema);
