const crypto = require('crypto');
const User = require('../models/Data');


exports.fetchData = async (req, res, next) => {
  try {
    const accounts = await User.find();

    res.send(accounts);
  } catch (error) {
    next(error);
  }
};
