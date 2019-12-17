import React from "react";
import styles from './Users.module.css'

let Users = (props) => {

    if (props.users.length === 0) {
        props.setUsers(
            [
                {
                    id: 1,
                    photoUrl: 'https://cdn.tvc.ru/pictures/o/364/134.jpg',
                    followed: false,
                    fullName: 'Eugene',
                    status: 'student',
                    location: {city: 'Moscow', country: 'Russia'}
                },
                {
                    id: 2,
                    photoUrl: 'https://cdn.tvc.ru/pictures/o/364/134.jpg',
                    followed: true,
                    fullName: 'Maks',
                    status: 'student',
                    location: {city: 'StPet', country: 'Russia'}
                },
                {
                    id: 3,
                    photoUrl: 'https://cdn.tvc.ru/pictures/o/364/134.jpg',
                    followed: true,
                    fullName: 'Eugene',
                    status: 'student',
                    location: {city: 'Bryansk', country: 'Russia'}
                },
            ]
        );
    }

    return (
        <div>
            {
                props.users.map(u => <div key={u.id}>
                    <span>
                        <div>
                            <img src={u.photoUrl} className={styles.userPhoto}/>
                        </div>
                        <div>
                            {u.followed
                                ? <button onClick={() => {
                                    props.unFollow(u.id)
                                }}>Unfollow</button>
                                : <button onClick={() => {
                                    props.follow(u.id)
                                }}>Follow</button>}

                        </div>
                    </span>
                    <span>
                        <span>
                            <div>
                                {u.fullName}
                            </div>
                            <div>
                                {u.status}
                            </div>
                        </span>
                        <span>
                            <div>{u.location.country}</div>
                            <div>{u.location.city}</div>
                        </span>
                    </span>
                </div>)
            }
        </div>
    )
};
export default Users;