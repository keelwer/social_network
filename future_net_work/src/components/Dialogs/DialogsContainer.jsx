import React from "react";
import s from './Dialogs.module.css'
import {NavLink} from "react-router-dom";
import {changeNewMessageTextActionCreater, sendMessageActionCreater} from "../../redux/dialogs_reducer";
import Dialogs from "./Dialogs";
import StoreContext from "../../StoreContext";

const DialogsContainer = () => {
    return (
        <StoreContext.Consumer>
            {
                (store) => {
                    let onSendMessageClick = () => {
                        store.dispatch(sendMessageActionCreater())
                    };
                    let onNewMessageChange = (text) => {
                        store.dispatch(changeNewMessageTextActionCreater(text))
                    };
                    return <Dialogs changeNewMessageText={onNewMessageChange}
                                    sendMessage={onSendMessageClick}
                                    dialogsPage={store.getState().dialogsPage}/>
                }
            }
        </StoreContext.Consumer>)
};
export default DialogsContainer;