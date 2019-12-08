import React from "react";
import s from './MyPosts.module.css'
import Post from "./Post/Post";

const MyPosts = () => {
    return <div className={s.content}>
        <div>My posts
            <div className={s.posts}>
                <textarea name="" id="" cols="20" rows="2"></textarea>
                <button>Add post</button>
                <button>Remove post</button>
            </div>
            <Post text={'hi world'}/>
            <Post text={'Cool React'}/>
            <Post text={'React-Redux'}/>
        </div>
    </div>
};
export default MyPosts;