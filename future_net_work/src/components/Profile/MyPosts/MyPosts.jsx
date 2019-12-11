import React from "react";
import s from './MyPosts.module.css'
import Post from "./Post/Post";
import {addPostActionCreater, changeNewPostTextActionCreater} from "../../../redux/profile_reducer";

const MyPosts = (props) => {

    let newPostElement = React.createRef();

    let Addpost = () => {
        props.dispatch(addPostActionCreater());
    };


    let onPostChange = () => {
        let text = newPostElement.current.value;
        props.dispatch(changeNewPostTextActionCreater(text));
    };

    let postElemeents = props.posts.posts.map(post => <Post text={post.message} like_counts={post.like_counts}/>);

    return <div className={s.content}>
        <div className={s.description}>
            My posts
            <div>
                <textarea onChange={onPostChange} ref={newPostElement} value={props.newPostText}/>
                <button onClick={Addpost}>Add post</button>
                <button>Remove post</button>
            </div>
            {postElemeents}
        </div>
    </div>
};

export default MyPosts;