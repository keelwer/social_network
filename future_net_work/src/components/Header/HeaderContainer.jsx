import React from "react";
import s from './Header.module.css'
import {NavLink} from "react-router-dom";
import Header from "./Header";
import * as axios from "axios";
import {connect} from "react-redux";
import {getAuthUserData, setAuthUserData} from "../../redux/auth-reducer";
import {authAPI} from "../../api/api";

class HeaderContainer extends React.Component {

    componentDidMount() {
        this.props.getAuthUserData()
    }

    render() {

        return <Header {...this.props}/>
    };
}

let mapStateToProps = (state) => ({
    isAuth: state.auth.isAuth,
    login: state.auth.login,

});

export default connect(mapStateToProps, {getAuthUserData})(HeaderContainer);