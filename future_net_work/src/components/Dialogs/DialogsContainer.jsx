import React from "react";
import {changeNewMessageTextActionCreater, sendMessageActionCreater} from "../../redux/dialogs_reducer";
import Dialogs from "./Dialogs";
import {connect} from "react-redux";
import {withAuthRedirect} from "../HOC/withAuthRedirect";

let mapStateToProps = (state) => {
    return{
        dialogsPage: state.dialogsPage,
    }
};

let AuthRedirectComponent = withAuthRedirect(Dialogs);

let mapDispatchToProps = (dispatch) => {
    return{
        changeNewMessageText: (text) => {
            dispatch(changeNewMessageTextActionCreater(text))
        },
        sendMessage: () => {
            dispatch(sendMessageActionCreater())
        },
    }
};


let DialogsContainer = connect(mapStateToProps, mapDispatchToProps)(AuthRedirectComponent);


export default DialogsContainer;