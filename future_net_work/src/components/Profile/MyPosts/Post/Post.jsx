import React from "react";
import s from './Post.module.css'

const Post = (props) => {
    return (
        <div className={s.content}>
            <div className={s.item}>
                <img src="https://avatars.mds.yandex.net/get-pdb/2196159/d8a9241d-506a-459d-b103-36dc376bf97d/s1200"
                     alt=""/>
                {props.text}
            </div>
            <div>
                {props.like_counts} like
            </div>
        </div>
    )
};
export default Post;