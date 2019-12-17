import styles from "./Users.module.css";
import photoAcc from "../../images/empty_acc.jpg";
import React from "react";


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
                            <img src={u.photos.small != null ? u.photos.small : photoAcc} className={styles.userPhoto}/>
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