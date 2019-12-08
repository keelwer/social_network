import React from "react";
import s from './Profile.module.css'
import MyPosts from "./MyPosts/MyPosts";

const Profile = () => {
    return (
        <div className={s.content}>
            <img src="https://avatars.mds.yandex.net/get-pdb/216365/eb43844b-51d6-41a0-86c0-0f3c47da5b48/s1200"
                 alt=""/>
            <div>
                ava
            </div>
            <MyPosts/>
        </div>
    )
};
export default Profile;