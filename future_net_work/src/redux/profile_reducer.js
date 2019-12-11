import sidebarReducer from "./sidebar_reducer";

const ADD_POST = 'ADD_POST';
const CHANGE_NEW_POST_TEXT = 'CHANGE_NEW_POST_TEXT';


export const profileReducer = (state, action) => {
    switch (action.type) {
        case ADD_POST:
            let newpost = {
                id: 4,
                message: state.newPostText,
                like_counts: 0,
            };
            state.posts.push(newpost);
            state.newPostText = '';
            return state;
        case CHANGE_NEW_POST_TEXT:
            state.newPostText = action.newText;
            return state;
        default:
            return state;
    }

};

export const addPostActionCreater = () => ({type: ADD_POST});
export const changeNewPostTextActionCreater = (text) => ({type: CHANGE_NEW_POST_TEXT, newText: text});

export default profileReducer;