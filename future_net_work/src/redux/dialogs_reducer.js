const CHANGE_NEW_MESSAGE_TEXT = 'CHANGE_NEW_MESSAGE_TEXT';
const SEND_MESSAGE = 'SEND_MESSAGE';

let initialState = {
    dialogs: [
        {id: 1, name: 'Eugene'},
        {id: 2, name: 'Eugene1'},
        {id: 3, name: 'Eugene2'},
        {id: 4, name: 'Eugene3'},
        {id: 5, name: 'Eugene4'},
        {id: 6, name: 'Eugene5'},
    ],
    message_data: [
        {id: 1, message: 'Hello React'},
        {id: 2, message: 'Hello React'},
    ]
};

export const dialogsReducer = (state = initialState, action) => {
    switch (action.type) {
        case CHANGE_NEW_MESSAGE_TEXT:
            return {
                ...state,
                newMessageChange: action.message,
            };
        case SEND_MESSAGE:
            let text = action.newMessageChange;
            return {
                ...state,
                message_data: [...state.message_data, {id: 3, message: text}],
            };
        default:
            return state;
    }
};


export const sendMessageActionCreater = (newMessageChange) => ({type: SEND_MESSAGE, newMessageChange});
export const changeNewMessageTextActionCreater = (text) => ({type: CHANGE_NEW_MESSAGE_TEXT, message: text});

export default dialogsReducer;