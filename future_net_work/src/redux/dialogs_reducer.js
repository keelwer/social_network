const CHANGE_NEW_MESSAGE_TEXT = 'CHANGE_NEW_MESSAGE_TEXT';
const SEND_MESSAGE = 'SEND_MESSAGE';

export const dialogsReducer = (state, action) => {
    switch (action.type) {
        case CHANGE_NEW_MESSAGE_TEXT:
            state.newMessageText = action.message;
            return state;
        case SEND_MESSAGE:
            let text = state.newMessageText;
            state.newMessageText = '';
            state.message_data.push({id: 3, message: text});
            return state;
        default:
            return state;
    }
};


export const sendMessageActionCreater = () => ({type: SEND_MESSAGE});
export const changeNewMessageTextActionCreater = (text) => ({type: CHANGE_NEW_MESSAGE_TEXT, message: text});

export default dialogsReducer;