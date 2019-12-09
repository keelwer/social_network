import React from "react";
import s from './Dialogs.module.css'
import {NavLink} from "react-router-dom";

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

    let dialogElements = props.dialogs.dialogs.map(dialog => <DialogItem name={dialog.name} id={dialog.id}/> );
    let messageElements = props.message_data.message_data.map(message => <Message message={message.name} id={message.id}/> );

    return (
        <div className={s.dialogs}>
            <div className={s.dialogsItems}>
                {dialogElements}
            </div>
            <div className={s.messages}>
                {messageElements}
            </div>
        </div>)
};
export default Dialogs;