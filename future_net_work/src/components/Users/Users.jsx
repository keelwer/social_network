import styles from "./Users.module.css";
import photoAcc from "../../images/empty_acc.jpg";
import React from "react";
import {NavLink} from "react-router-dom";
import * as axios from "axios";
import {toggleIsFollowingInProgress} from "../../redux/users_reducer";


let Users = (props) => {

    let pagesCount = Math.ceil(props.totalUserCount / props.pageSize);

    let pages = [];
    for (let i = 1; i <= pagesCount; i++) {
        pages.push(i);
    }

    return (
        <div>
            <div>
                {pages.map(p => {
                    return <span className={props.currentPage === p && styles.selectPage} onClick={(e) => {
                        props.onPageChange(p)
                    }}>{p}</span>
                })}
            </div>
            {
                props.users.map(u => <div key={u.id}>
                    <span>
                        <div>
                            <NavLink to={'/profile/' + u.id}><img
                                src={u.photos.small != null ? u.photos.small : photoAcc}
                                className={styles.userPhoto}/>
                            </NavLink>
                        </div>
                        <div>
                            {u.followed
                                ? <button disabled={props.followingInProgress.some(id => id === u.id)} onClick={() => {
                                    props.toggleIsFollowingInProgress(true, u.id);
                                    axios.delete(`https://social-network.samuraijs.com/api/1.0/follow/${u.id}`, {
                                        withCredentials: true,
                                        headers: {"API-KEY": "5ffffc5c-ac7f-444a-ad2c-673d8d1f9696"}
                                    })
                                        .then(response => {
                                            if (response.data.resultCode == 0) {
                                                props.unFollow(u.id)
                                            }
                                            props.toggleIsFollowingInProgress(false, u.id);

                                        });


                                }}>Unfollow</button>
                                : <button disabled={props.followingInProgress.some(id => id === u.id)} onClick={() => {
                                    props.toggleIsFollowingInProgress(true, u.id);
                                    axios.post(`https://social-network.samuraijs.com/api/1.0/follow/${u.id}`, {}, {
                                        withCredentials: true,
                                        headers: {"API-KEY": "5ffffc5c-ac7f-444a-ad2c-673d8d1f9696"}
                                    })
                                        .then(response => {
                                            if (response.data.resultCode == 0) {
                                                props.follow(u.id)
                                            }
                                            props.toggleIsFollowingInProgress(false, u.id);
                                        });


                                }}>Follow</button>}

                        </div>
                    </span>
                    <span>
                        <span>
                            <div>
                                {u.name}
                            </div>
                            <div>
                                {u.status}
                            </div>
                        </span>
                        <span>
                            <div>{"u.location.country"}</div>
                            <div>{"u.location.city"}</div>
                        </span>
                    </span>
                </div>)
            }
        </div>
    )
};

export default Users;