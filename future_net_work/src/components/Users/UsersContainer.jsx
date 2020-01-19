import React from "react";
import {connect} from "react-redux";
import {
    follow, getUsers,
    setCurrentPage,
    setUsers,
    setUsersTotalCount,
    toggleIsFetching, toggleIsFollowingInProgress,
    unfollow
} from "../../redux/users_reducer";
import * as axios from "axios";
import Users from "./Users";
import Preloader from "../common/Preloader/Preloader";
import {userAPI} from "../../api/api";
import {compose} from "redux";
import {withAuthRedirect} from "../HOC/withAuthRedirect";

class UsersContainer extends React.Component {

    componentDidMount() {
        this.props.getUsers(this.props.currentPage, this.props.pageSize);
    }

    onPageChange = (PageNumber) => {
        this.props.setCurrentPage(PageNumber);
        this.props.getUsers(PageNumber, this.props.pageSize);
    };

    render() {
        return <>
            {this.props.isFetching ? <Preloader/> : null}
            <Users totalUserCount={this.props.totalUserCount}
                   pageSize={this.props.pageSize}
                   currentPage={this.props.currentPage}
                   onPageChange={this.onPageChange}
                   users={this.props.users}
                   follow={this.props.follow}
                   unfollow={this.props.unfollow}
                   followingInProgress={this.props.followingInProgress}
            />
        </>
    }
}

const mapStateToProps = (state) => {
    return {
        users: state.usersPage.users,
        pageSize: state.usersPage.pageSize,
        totalUserCount: state.usersPage.totalUserCount,
        currentPage: state.usersPage.currentPage,
        isFetching: state.usersPage.isFetching,
        followingInProgress: state.usersPage.followingInProgress
    }
};


export default compose(
    withAuthRedirect,
    connect(mapStateToProps, {
        follow,
        unfollow,
        setUsers,
        setCurrentPage,
        setUsersTotalCount,
        toggleIsFetching,
        toggleIsFollowingInProgress,
        getUsers
    })
)(UsersContainer);