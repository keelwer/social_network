import React from "react";
import s from './MyPosts.module.css'
import Post from "./Post/Post";
import {Field, reduxForm} from "redux-form";
import {maxLength30, maxLengthCreator, required} from "../../../utils/validators/validators";
import {Textarea} from "../../common/FormsControl/FormsControl";

class MyPosts extends React.Component {
    shouldComponentUpdate(nextProps, nextState) {
        return nextProps != this.props && nextState != this.state;
    }


    render() {

        let addNewPost = (values) => {
            this.props.addPost(values.newMessagePost);
        };

        let postElements = this.props.posts.map(post => <Post text={post.message} key={post.id}
                                                              like_counts={post.like_counts}/>);

        return <div className={s.content}>
            <div className={s.description}>
                My posts
                <AddMessagePostReduxForm onSubmit={addNewPost}/>
                {postElements}
            </div>
        </div>
    }
}


const maxLegth10 = maxLengthCreator(10);


const AddPostForm = (props) => {
    return (
        <form onSubmit={props.handleSubmit}>
            <div>
                <Field component={Textarea} name='newMessagePost' placeholder='Enter your message'
                validate={[required, maxLegth10]}/>
            </div>
            <div>
                <button>Add post</button>
            </div>
        </form>
    )
}

const AddMessagePostReduxForm = reduxForm({form: 'newMessagePost'})(AddPostForm);

export default MyPosts;