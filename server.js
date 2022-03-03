const express = require('express');
const dotenv = require('dotenv');
const morgan = require('morgan');
const connectDB = require('./config/db');
// const authRoute = require('./routes/auth');
// const adminRoute = require('./routes/admin');
// const credentialRoute = require('./routes/credentials');
// const shareRoute = require('./routes/share');
// const miscRoute = require('./routes/misc');
// const convertRoute = require('./routes/convert');
// const paymentRoute = require('./routes/payment');



const connectDB = require('./config/db');

// Initialize Express
const app = express();

//Middlewares
app.use(express.json());

if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}



const PORT = process.env.PORT || 5000;

app.listen(
  PORT,
  console.log(
    `Server running in ${process.env.NODE_ENV} mode on http://localhost:${PORT}`
  )
);