import React, { Fragment } from 'react';
import './App.scss';

import Header from './components/Header';
import Table from './components/Table';

const driversData = [
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
  {
    number: 'SOL_USDT',
    name: 46954.71,
    team: 46880.01,
    country: 46904.98,
    dob: 2.01899437,
    placeOfBirth: 46889.46,
  },
];

const tracksData = [
  {
    name: 'Spa-Francorchamps',
    country: 'Belgium',
    length: 7.004,
    numberOfLaps: 44,
  },
  {
    name: 'Circuit de Monaco',
    country: 'Monaco',
    length: 3.337,
    numberOfLaps: 78,
  },
  {
    name: 'Silverstone',
    country: 'England',
    length: 5.891,
    numberOfLaps: 52,
  },
  {
    name: 'Suzuka',
    country: 'Japan',
    length: 5.807,
    numberOfLaps: 53,
  },
  {
    name: 'Hockenheimring',
    country: 'Germany',
    length: 4.574,
    numberOfLaps: 67,
  },
];

const App = () => {
  return (
    <Fragment>
      <Header title='DAVID_CRYPTO_MA' />
      <Table
        tableData={driversData}
        headingColumns={['Symbols', '5MIN', '15MIN', '1HRS', '4HRS', '1DAY']}
        title='SYMBOLS, PERIODS &amp; MA'
      />
      <Table
        tableData={tracksData}
        headingColumns={['Name', 'Country', 'Length(km)', 'Number of laps']}
        title='Top F1 tracks'
        breakOn='small'
      />
    </Fragment>
  );
};

export default App;
