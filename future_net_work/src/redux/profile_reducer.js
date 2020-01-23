import sidebarReducer from "./sidebar_reducer";
import {profileAPI, userAPI} from "../api/api";

const ADD_POST = 'ADD_POST';
const CHANGE_NEW_POST_TEXT = 'CHANGE_NEW_POST_TEXT';
const SET_USER_PROFILE = 'SET_USER_PROFILE';
const SET_STATUS = 'SET_STATUS';

let initialState = {
    posts: [
        {id: 1, message: 'hi world', like_counts: 1},
        {id: 2, message: 'Cool React', like_counts: 9},
        {id: 3, message: 'React-Redux', like_counts: 5},
    ],
    newPostText: 'React+Redux',
    profile: null,
    status: '',
};

export const profileReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_POST: {
            let newpost = {
                id: 4,
                message: state.newPostText,
                like_counts: 0,
            };
            return {
                ...state,
                posts: [...state.posts, newpost],
                newPostText: ''
            };
        }
        case CHANGE_NEW_POST_TEXT: {
            return {
                ...state,
                newPostText: action.newText
            };
        }
        case SET_STATUS: {
            return {
                ...state,
                status: action.status
            };
        }
        case SET_USER_PROFILE: {
            return {
                ...state,
                profile: action.profile
            };
        }
        default:
            return state;
    }

};

export const addPostActionCreater = () => ({type: ADD_POST});
export const setUserProfile = (profile) => ({type: SET_USER_PROFILE, profile});
export const setStatus = (status) => ({type: SET_STATUS, status});
export const getUserProfile = (userId) => (dispatch) => {
    userAPI.getProfile(userId).then(response => {
        dispatch(setUserProfile(response.data));
    })
};

export const getStatus = (userId) => (dispatch) => {
    profileAPI.getStatus(userId).then(response => {
        dispatch(setStatus(response.data));
    })
};

export const updateStatus = (status) => (dispatch) => {
    profileAPI.updateStatus(status).then(response => {
        if (response.data.resultcode === 0) {
            dispatch(setStatus(status));
        }
    })
};

export const changeNewPostTextActionCreater = (text) => ({type: CHANGE_NEW_POST_TEXT, newText: text});

export default profileReducer;