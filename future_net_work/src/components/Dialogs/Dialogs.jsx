import React from "react";
import s from './Dialogs.module.css'
import {NavLink, Redirect} from "react-router-dom";
import {Field, reduxForm} from "redux-form";

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
    let state = props.dialogsPage;

    let dialogElements = state.dialogs.map(dialog => <DialogItem name={dialog.name} key={dialog.id} id={dialog.id}/>);
    let messageElements = state.message_data.map(message => <Message message={message.message}
                                                                     id={message.id}/>);

    let addNewMessage = (values) => {
        props.sendMessage(values.newMessageChange);
    };

    return (
        <div className={s.dialogs}>
            <div className={s.dialogsItems}>
                {dialogElements}
            </div>
            <div className={s.messages}>
                <div>{messageElements}</div>
                <AddMessageReduxForm onSubmit={addNewMessage}/>
            </div>
        </div>)
};

const AddMessageForm = (props) => {
    return (
        <form onSubmit={props.handleSubmit}>
            <div>
                <Field component='textarea' name='newMessageChange' placeholder='Enter your message'/>
            </div>
            <div>
                <button>Send</button>
            </div>
        </form>
    )
}

const AddMessageReduxForm = reduxForm({form: 'dialogAddMessageForm'})(AddMessageForm);

export default Dialogs;