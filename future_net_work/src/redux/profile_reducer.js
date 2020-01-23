
import {profileAPI, userAPI} from "../api/api";

const ADD_POST = 'ADD_POST';
const SET_USER_PROFILE = 'SET_USER_PROFILE';
const SET_STATUS = 'SET_STATUS';

let initialState = {
    posts: [
        {id: 1, message: 'hi world', like_counts: 1},
        {id: 2, message: 'Cool React', like_counts: 9},
        {id: 3, message: 'React-Redux', like_counts: 5},
    ],
    profile: null,
    status: '',
};

export const profileReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_POST: {
            let newpost = {
                id: 4,
                message: action.newMessagePost,
                like_counts: 0,
            };
            return {
                ...state,
                posts: [...state.posts, newpost],
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

export const addPostActionCreater = (newMessagePost) => ({type: ADD_POST, newMessagePost});
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

export default profileReducer;