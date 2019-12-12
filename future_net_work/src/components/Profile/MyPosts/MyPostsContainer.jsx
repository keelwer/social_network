import React from "react";
import Post from "./Post/Post";
import {addPostActionCreater, changeNewPostTextActionCreater} from "../../../redux/profile_reducer";
import MyPosts from "./MyPosts";
import StoreContext from "../../../StoreContext";

const MyPostsContainer = (props) => {


    return (
        <StoreContext.Consumer>{
            (store) => {
                let state = props.store.getState();

                let addPost = () => {
                    props.store.dispatch(addPostActionCreater());
                };

                let onPostChange = (text) => {
                    let action = changeNewPostTextActionCreater(text);
                    props.store.dispatch(action);
                };

                return <MyPosts changeNewPostText={onPostChange} addPost={addPost} posts={state.profilePage.posts}
                         newPostText={state.profilePage.newPostText}/>
            }


        }
        </StoreContext.Consumer>)
};

export default MyPostsContainer;