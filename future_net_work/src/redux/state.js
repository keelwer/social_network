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
            message_data: [
                {id: 1, name: 'Hello React'},
                {id: 2, name: 'Hello React'},
            ],
            dialogs: [
                {id: 1, name: 'Eugene'},
                {id: 2, name: 'Eugene1'},
                {id: 3, name: 'Eugene2'},
                {id: 4, name: 'Eugene3'},
                {id: 5, name: 'Eugene4'},
                {id: 6, name: 'Eugene5'},
            ],
        },

    },
    _rerenderTree() {
        console.log('State changed')
    },
    getState() {
        return this._state;
    },
    subscribe(observer) {
        this._rerenderTree = observer;
    },

    dispatch(action) {
        if (action.type === 'ADD_POST') {
            let newpost = {
                id: 4,
                message: this._state.profilePage.newPostText,
                like_counts: 0,
            };
            this._state.profilePage.posts.push(newpost);
            this._state.profilePage.newPostText = '';
            this._rerenderTree(this._state)
        } else if (action.type === 'CHANGE-NEW-POST-TEXT') {
            this._state.profilePage.newPostText = action.newText;
            this._rerenderTree(this._state)
        }
    },

};
window.store = store;

export default store;