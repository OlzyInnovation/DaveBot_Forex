const mongoose = require('mongoose');

const connectDB = async () => {
  await mongoose.connect("mongodb://localhost:27017/David_Crypto_MA", {
    useNewUrlParser: true,
    useCreateIndex: true,
    useUnifiedTopology: true,
    useFindAndModify: true,
  });
  console.log(`MongoDB connected`);
};

module.exports = connectDB;
