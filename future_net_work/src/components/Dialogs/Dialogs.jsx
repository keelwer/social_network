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
    return (
        <div className={s.dialogs}>
            <div className={s.dialogsItems}>
                <DialogItem name='Eugene' id='1'/>
                <DialogItem name='Dmitriy' id='2'/>
                <DialogItem name='Semen' id='3'/>
                <DialogItem name='Olga' id='4'/>
            </div>
            <div className={s.messages}>
                <Message message={'Hello React'}/>
                <Message message={'Hello Redux'}/>
                <Message message={'Hello all'}/>
                <Message message={'Hello React'}/>
            </div>
        </div>)
};
export default Dialogs;