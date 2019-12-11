import React from 'react';
import './App.css';
import Header from "./components/Header/Header";
import Navbar from "./components/NavBar/Navbar";
import Profile from "./components/Profile/Profile";
import Dialogs from "./components/Dialogs/Dialogs";
import {Route, BrowserRouter} from "react-router-dom";
import News from "./components/News/News";
import Music from "./components/Music/Music";
import store, {subscribe} from "./redux/store";


function App(props) {


    return (
        <BrowserRouter>
            <div className='app-wrapper'>
                <Header/>
                <Navbar/>
                <div className='app-wrapper-content'>
                    <Route path='/profile'
                           render={() => <Profile store={props.store}/>}/>
                    <Route path='/dialogs' render={() => <Dialogs store={props.store}/>}/>
                    <Route path='/news' render={() => <News/>}/>
                    <Route path='/music' render={() => <Music/>}/>
                </div>
            </div>
        </BrowserRouter>)
}



export default App;
