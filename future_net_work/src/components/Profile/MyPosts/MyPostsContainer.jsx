import React from "react";
import Post from "./Post/Post";
import {addPostActionCreater, changeNewPostTextActionCreater} from "../../../redux/profile_reducer";
import MyPosts from "./MyPosts";
import StoreContext from "../../../StoreContext";

const MyPostsContainer = () => {
    return (
        <StoreContext.Consumer>{
            (store) => {
                let state = store.getState();

                let addPost = () => {
                    store.dispatch(addPostActionCreater());
                };

                let onPostChange = (text) => {
                    let action = changeNewPostTextActionCreater(text);
                    store.dispatch(action);
                };

                return <MyPosts changeNewPostText={onPostChange} addPost={addPost} posts={state.profilePage.posts}
                         newPostText={state.profilePage.newPostText}/>
            }


        }
        </StoreContext.Consumer>)
};

export default MyPostsContainer;