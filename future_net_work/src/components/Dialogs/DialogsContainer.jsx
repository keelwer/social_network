import React from "react";
import {changeNewMessageTextActionCreater, sendMessageActionCreater} from "../../redux/dialogs_reducer";
import Dialogs from "./Dialogs";
import {connect} from "react-redux";
import {withAuthRedirect} from "../HOC/withAuthRedirect";
import {compose} from "redux";

let mapStateToProps = (state) => {
    return {
        dialogsPage: state.dialogsPage,
    }
};


let mapDispatchToProps = (dispatch) => {
    return {
        changeNewMessageText: (text) => {
            dispatch(changeNewMessageTextActionCreater(text))
        },
        sendMessage: (newMessageChange) => {
            dispatch(sendMessageActionCreater(newMessageChange))
        },
    }
};


export default compose(
    withAuthRedirect,
    connect(mapStateToProps, mapDispatchToProps),
)(Dialogs);