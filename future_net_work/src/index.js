import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import store from "./redux/state";

let rerenderTree = () => {
    ReactDOM.render(<App appState={store.getState()} addPost={store.AddPost.bind(store)} changeNewPostText={store.changeNewPostText.bind(store)}/>, document.getElementById('root'));
};

rerenderTree(store.getState);

store.subscribe(rerenderTree);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
