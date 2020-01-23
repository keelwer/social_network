import React from "react";
import Post from "./Post/Post";
import {addPostActionCreater, changeNewPostTextActionCreater} from "../../../redux/profile_reducer";
import MyPosts from "./MyPosts";
import {changeNewMessageTextActionCreater, sendMessageActionCreater} from "../../../redux/dialogs_reducer";
import {connect} from "react-redux";



const mapStateToProps = (state) => {
    return{
        posts: state.profilePage.posts,
        newPostText: state.profilePage.newPostText,
    }
};

const mapDispatchToProps = (dispatch) => {
    return{
        addPost: (newMessagePost) => {
            dispatch(addPostActionCreater(newMessagePost))
        }
    }
};


let MyPostsContainer = connect(mapStateToProps, mapDispatchToProps)(MyPosts);





export default MyPostsContainer;