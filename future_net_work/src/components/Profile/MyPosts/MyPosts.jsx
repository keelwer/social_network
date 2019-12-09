import React from "react";
import s from './MyPosts.module.css'
import Post from "./Post/Post";




const MyPosts = (props) => {

    let Addpost = () => {
        let text = newPostElement.current.value;
        alert('Hey react')};

    let newPostElement = React.createRef();

    let postElemeents = props.posts.map(post => <Post text={post.message} like_counts={post.like_counts}/>);

    return <div className={s.content}>
        <div className={s.description}>
            My posts
            <div>
                <textarea ref={newPostElement}> </textarea>
                <button onClick={ Addpost }>Add post</button>
                <button>Remove post</button>
            </div>
            {postElemeents}
        </div>
    </div>
};
export default MyPosts;