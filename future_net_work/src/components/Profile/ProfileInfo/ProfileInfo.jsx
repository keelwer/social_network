import React from "react";
import s from './ProfileInfo.module.css'
import Preloader from "../../common/Preloader/Preloader";


const ProfileInfo = (props) => {
    if (!props.profile) {
        return <Preloader/>
    }
    return (
        <div>
            <img src="https://avatars.mds.yandex.net/get-pdb/216365/eb43844b-51d6-41a0-86c0-0f3c47da5b48/s1200"
                 alt=""/>
            <div className={s.description}>
                <img src={props.profile.photos.large} alt=""/>
                ava
            </div>
        </div>
    )
};
export default ProfileInfo;