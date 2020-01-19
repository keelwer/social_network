import React from "react";
import {changeNewMessageTextActionCreater, sendMessageActionCreater} from "../../redux/dialogs_reducer";
import Dialogs from "./Dialogs";
import {connect} from "react-redux";

let mapStateToProps = (state) => {
    return{
        dialogsPage: state.dialogsPage,
        isAuth: state.auth.isAuth,
    }
};

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


let DialogsContainer = connect(mapStateToProps, mapDispatchToProps)(Dialogs);


export default DialogsContainer;