// Register.jsx
import React from "react";

require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import TextField from 'material-ui/TextField';
import Loyalty from 'material-ui/svg-icons/action/loyalty';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import FlatButton from 'material-ui/FlatButton';


export default class Register extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            email: '',
            pwd: '',
            username: '',
            sex: 'women'
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        let value =  event.target.value;
        let name = event.target.name;
        this.setState({
            [name]: value
        });
    }

    handleSubmit(event) {
        // alert('A name was submitted: ' + this.state.value);
        event.preventDefault();
        let email = this.state.email;
        let pwd = this.state.pwd;
        let username = this.state.username;
        let sex = this.state.sex;

        fetch(window.location.origin + '/api/register', {
            method: 'post',
            body: JSON.stringify({
                email: email,
                pwd: pwd,
                sex: sex,
                username: username
            })
        }).then(function(response) { return response.json(); })
            .then(function(data) {
                console.log(data);
                if (data === true) {
                    alert('successfully registered');
                } else {
                    alert('registration failed');
                }
            });
    }

    render() {
        return (
            <MuiThemeProvider>
                <div>
                    <div className="register-form">
                        <p>Welcome to Garms app !</p>
                        <TextField
                            hintText="Your name"
                            name="username"
                            floatingLabelText="Input your first name:"
                            onChange={this.handleChange.bind(this)}
                        />
                        <br></br>
                        <br></br>
                        <RadioButtonGroup
                            name="sex"
                            defaultSelected="women"
                            onChange={this.handleChange.bind(this)}
                        >
                            <RadioButton
                                value="women"
                                label="Woman"
                                checkedIcon={<Loyalty style={{color: '#9276b5'}}/>}
                                uncheckedIcon={<Loyalty/>}
                                labelStyle={{textAlign: 'left'}}
                            />
                            <RadioButton
                                value="men"
                                label="Man"
                                checkedIcon={<Loyalty style={{color: '#9276b5'}}/>}
                                uncheckedIcon={<Loyalty/>}
                                labelStyle={{textAlign: 'left'}}
                            />
                        </RadioButtonGroup>
                        <TextField
                            name="email"
                            hintText="Your e-mail"
                            floatingLabelText="Input your e-mail address:"
                            onChange={this.handleChange.bind(this)}
                        />
                        <br></br>
                        <TextField
                            name="pwd"
                            hintText="Password"
                            floatingLabelText="Choose a password:"
                            type="password"
                            onChange={this.handleChange.bind(this)}
                        />
                        <br></br>
                        <FlatButton label="register" onClick={this.handleSubmit} />
                    </div>
                </div>
            </MuiThemeProvider>
        );
    }
}
