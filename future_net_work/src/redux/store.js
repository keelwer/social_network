// import profileReducer from "./profile_reducer";
// import dialogsReducer from "./dialogs_reducer";
// import sidebarReducer from "./sidebar_reducer";
//
// let store = {
//     _state: {
//         profilePage: {
//             posts: [
//                 {id: 1, message: 'hi world', like_counts: 1},
//                 {id: 2, message: 'Cool React', like_counts: 9},
//                 {id: 2, message: 'React-Redux', like_counts: 5},
//             ],
//             newPostText: 'React+Redux'
//         },
//         dialogsPage: {
//             dialogs: [
//                 {id: 1, name: 'Eugene'},
//                 {id: 2, name: 'Eugene1'},
//                 {id: 3, name: 'Eugene2'},
//                 {id: 4, name: 'Eugene3'},
//                 {id: 5, name: 'Eugene4'},
//                 {id: 6, name: 'Eugene5'},
//             ],
//             message_data: [
//                 {id: 1, message: 'Hello React'},
//                 {id: 2, message: 'Hello React'},
//             ],
//             newMessageText: '',
//         },
//         sidebar: {},
//     },
//     _callSubscriber() {
//         console.log('State changed')
//     },
//     getState() {
//         return this._state;
//     },
//     subscribe(observer) {
//         this._callSubscriber = observer;
//     },
//
//     dispatch(action) {
//
//         this._state.profilePage = profileReducer(this._state.profilePage, action);
//         this._state.dialogsPage = dialogsReducer(this._state.dialogsPage, action);
//         this._state.sidebar = sidebarReducer(this._state.sidebar, action);
//         this._callSubscriber(this._state);
//
//     }
//
// };
//
//
//
//
//
//
//
// window.store = store;
//
// export default store;