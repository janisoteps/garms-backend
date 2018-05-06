// Register.jsx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import TextField from 'material-ui/TextField';


export default class Register extends React.Component  {
  constructor(props) {
    super(props);
  }

  render () {
    return (
      <MuiThemeProvider>
        <div>
          <div className="register-form">
            <p>Welcome to Garms app !</p>
            <TextField hintText="Your name" floatingLabelText="Input your first name:"/>
            <br></br>
            <TextField hintText="Your e-mail" floatingLabelText="Input your e-mail address:"/>
            <br></br>
            <TextField hintText="Password" floatingLabelText="Choose a password:" type="password"/>
          </div>
        </div>
      </MuiThemeProvider>
    );
  }
}
