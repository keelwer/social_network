let rerenderTree = () => {

};

let state = {
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

};

export const AddPost = () => {
    let newpost = {
        id: 4,
        message: state.profilePage.newPostText,
        like_counts: 0,
    };
    state.profilePage.posts.push(newpost);
    state.profilePage.newPostText = '';
    rerenderTree(state)
};

export const changeNewPostText = (newText) => {
    state.profilePage.newPostText = newText;
    rerenderTree(state)
};

export  const subscribe = (observer) => {
    rerenderTree = observer;
};
export default state