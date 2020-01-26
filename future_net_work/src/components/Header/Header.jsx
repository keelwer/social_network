import React from "react";
import s from './Header.module.css'
import {NavLink} from "react-router-dom";

const Header = (props) => {
    return <header className={s.header}>
        <img src='https://avatars.mds.yandex.net/get-pdb/2128437/12d43701-d95d-4052-aaf1-f5ec0de1a23f/s1200'/>
        <div className={s.loginBlock}>
            {props.isAuth ? <div>{props.login} - <button onClick={props.logout}>Logout</button></div> : <NavLink to={'/login'}>Login</NavLink> }
        </div>
    </header>
};
export default Header;