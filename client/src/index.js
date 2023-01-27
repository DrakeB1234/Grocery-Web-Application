import React from 'react';
import ReactDOM from 'react-dom/client';

// global css
import './index.css';

// component imports
import Nav from './modules/Nav';

// page imports
import Login from './loginreg/Login';
import Signup from './loginreg/Signup';
// import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Login />
  </React.StrictMode>
);

// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
