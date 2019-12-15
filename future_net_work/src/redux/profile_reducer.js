import sidebarReducer from "./sidebar_reducer";

const ADD_POST = 'ADD_POST';
const CHANGE_NEW_POST_TEXT = 'CHANGE_NEW_POST_TEXT';

let initialState = {
    posts: [
        {id: 1, message: 'hi world', like_counts: 1},
        {id: 2, message: 'Cool React', like_counts: 9},
        {id: 3, message: 'React-Redux', like_counts: 5},
    ],
    newPostText: 'React+Redux'
};

export const profileReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_POST: {
            let newpost = {
                id: 4,
                message: state.newPostText,
                like_counts: 0,
            };
            return  {
                ...state,
                posts: [...state.posts, newpost],
                newPostText: ''
            };
        }
        case CHANGE_NEW_POST_TEXT: {
            return  {
                ...state,
                newPostText: action.newText
            };
        }
        default:
            return state;
    }

};

export const addPostActionCreater = () => ({type: ADD_POST});
export const changeNewPostTextActionCreater = (text) => ({type: CHANGE_NEW_POST_TEXT, newText: text});

export default profileReducer;