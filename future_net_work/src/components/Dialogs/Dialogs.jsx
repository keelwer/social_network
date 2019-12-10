import React from "react";
import s from './Dialogs.module.css'
import {NavLink} from "react-router-dom";
import {changeNewMessageTextActionCreater, sendMessageActionCreater} from "../../redux/state";

const DialogItem = (props) => {
    let path = '/dialogs/' + props.id;
    return (
        <div className={s.dialog + ' ' + s.active}>
            <NavLink to={path}>{props.name}</NavLink>
        </div>
    )
};

const Message = (props) => {
    return (
        <div className={s.dialog}>
            {props.message}
        </div>
    )
};


const Dialogs = (props) => {

    let state = props.store.getState().dialogsPage;

    let dialogElements = state.dialogs.map(dialog => <DialogItem name={dialog.name} id={dialog.id}/>);
    let messageElements = state.message_data.map(message => <Message message={message.message}
                                                                                  id={message.id}/>);
    let newMessageText = state.newMessageText;

    let onSendMessageClick = () => {
        props.store.dispatch(sendMessageActionCreater())
    };
    let onNewMessageChange = (e) => {
        let text = e.target.value;
        props.store.dispatch(changeNewMessageTextActionCreater(text))
    };

    return (
        <div className={s.dialogs}>
            <div className={s.dialogsItems}>
                {dialogElements}
            </div>
            <div className={s.messages}>
                <div>{messageElements}</div>
                <div>
                    <div><textarea placeholder='Enter your message'
                                   onChange={onNewMessageChange}
                                   value={newMessageText}
                                   cols="30"
                                   rows="10"/></div>
                    <div>
                        <button onClick={onSendMessageClick}>Send</button>
                    </div>
                </div>
            </div>
        </div>)
};
export default Dialogs;