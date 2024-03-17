import React from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';

function App() {
  return (
  <div className="App">
    <div className="row">
      <Sidebar/>
      <MainContent/>
    </div>
  </div>
);
}

export default App;
