import React, { useEffect, useState } from 'react';
import './App.css';
import { BasicTable } from './components/BasicTable';

function App() {
  const [data, setData] = useState([]);
  const fetchData = () => {
    fetch('http://localhost:5000/', {
      'Content-Type': 'application/json',
    })
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  };
  useEffect(() => {
    setTimeout(() => {
      fetchData();
    }, 3);
  }, []);

  return (
    <>
      <BasicTable data={data} />
    </>
  );
}

export default App;
