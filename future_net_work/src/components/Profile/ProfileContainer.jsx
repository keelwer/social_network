import React from "react";
import Profile from "./Profile";
import * as axios from "axios";
import {connect} from "react-redux";
import {getUserProfile} from "../../redux/profile_reducer";
import {Redirect, withRouter} from "react-router-dom";
import {userAPI} from "../../api/api";
import {withAuthRedirect} from "../HOC/withAuthRedirect";
import {compose} from "redux";

class ProfileContainer extends React.Component {

    componentDidMount() {
        let userId = this.props.match.params.userId;
        if (!userId) {
            userId = 2;
        }
        this.props.getUserProfile(userId)
    }


    render() {
        return (

            <Profile {...this.props} profile={this.props.profile}/>
        )
    }
};


let mapStateToProps = (state) => ({
    profile: state.profilePage.profile,

});

export default compose(
    withRouter,
    connect(mapStateToProps, {getUserProfile}),
    withAuthRedirect,
)(ProfileContainer);