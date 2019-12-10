const ADD_POST = 'ADD_POST';
const CHANGE_NEW_POST_TEXT = 'CHANGE_NEW_POST_TEXT';
const CHANGE_NEW_MESSAGE_TEXT = 'CHANGE_NEW_MESSAGE_TEXT';
const SEND_MESSAGE = 'SEND_MESSAGE';

let store = {
    _state: {
        profilePage: {
            posts: [
                {id: 1, message: 'hi world', like_counts: 1},
                {id: 2, message: 'Cool React', like_counts: 9},
                {id: 2, message: 'React-Redux', like_counts: 5},
            ],
            newPostText: 'React+Redux'
        },
        dialogsPage: {
            dialogs: [
                {id: 1, name: 'Eugene'},
                {id: 2, name: 'Eugene1'},
                {id: 3, name: 'Eugene2'},
                {id: 4, name: 'Eugene3'},
                {id: 5, name: 'Eugene4'},
                {id: 6, name: 'Eugene5'},
            ],
            message_data: [
                {id: 1, message: 'Hello React'},
                {id: 2, message: 'Hello React'},
            ],
            newMessageText: '',
        },

    },
    _callSubscriber() {
        console.log('State changed')
    },
    getState() {
        return this._state;
    },
    subscribe(observer) {
        this._callSubscriber = observer;
    },

    dispatch(action) {
        if (action.type === ADD_POST) {
            let newpost = {
                id: 4,
                message: this._state.profilePage.newPostText,
                like_counts: 0,
            };
            this._state.profilePage.posts.push(newpost);
            this._state.profilePage.newPostText = '';
            this._callSubscriber(this._state)
        } else if (action.type === CHANGE_NEW_POST_TEXT) {
            this._state.profilePage.newPostText = action.newText;
            this._callSubscriber(this._state)
        } else if (action.type === CHANGE_NEW_MESSAGE_TEXT) {
            this._state.dialogsPage.newMessageText = action.newText;
            this._callSubscriber(this._state)
        } else if (action.type === SEND_MESSAGE) {
            let text = this._state.dialogsPage.newMessageText;
            this._state.dialogsPage.newMessageText = '';
            this._state.dialogsPage.message_data.push({id: 5, message: text});
            this._callSubscriber(this._state)
        }
    }

};


export const addPostActionCreater = () => ({type: ADD_POST});
export const changeNewPostTextActionCreater = (text) => ({type: CHANGE_NEW_POST_TEXT,newText: text});

export const sendMessageActionCreater = () => ({type: SEND_MESSAGE});
export const changeNewMessageTextActionCreater = (text) => ({type: CHANGE_NEW_MESSAGE_TEXT,message: text});


window.store = store;

export default store;