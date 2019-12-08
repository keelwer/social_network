import React from "react";
import s from './MyPosts.module.css'
import Post from "./Post/Post";

const MyPosts = () => {
    return <div className={s.content}>
        <div>My posts
            <div>
                <textarea name="" id="" cols="20" rows="2"></textarea>
                <button>Add post</button>
                <button>Remove post</button>
            </div>
            <Post text={'hi world'} like_counts={1}/>
            <Post text={'Cool React'} like_counts={90}/>
            <Post text={'React-Redux'} like_counts={4}/>
        </div>
    </div>
};
export default MyPosts;