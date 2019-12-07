import React from 'react';
import './App.css';
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import MainContent from "./components/MainContent";


function App() {
    return (
        <div className='app-wrapper'>
            <Header/>
            <Navbar/>
            <MainContent/>
        </div>
    );
}

export default App;
