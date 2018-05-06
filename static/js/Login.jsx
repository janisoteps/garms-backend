// Register.jsx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Route } from 'react-router-dom'

class Login extends React.Component  {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };

  constructor(props) {
    super(props);
    const { cookies } = this.props;
    this.state = {
      isAuth: cookies.get('isAuth'),
      email: '',
      pwd: ''
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    // this.setLoginState = this.props.setLoginState;
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

    fetch(window.location.origin + '/api/login', {
      method: 'post',
      body: JSON.stringify({email: email, pwd: pwd})
    }).then(function(response) { return response.json(); })
      .then(function(data) {
        console.log(data);
        if (data === "OK") {
          // this.setLoginState();
          this.setState({
            isAuth: true
          });
        }
      });
  }


  render () {
    // var setLoginState = this.props.setLoginState;
    console.log('Login file isAuth', this.state.isAuth);
    const loginForm = this.state.isAuth === true || this.state.isAuth == "true" ? (
      <Route render={({ history }) => (
        <div className="login-welcome" onClick={() => { history.push('/') }}>
          <h2>
            Welcome to Garms app
          </h2>
          <br></br>
          <h3>
            Start Eploring
          </h3>
        </div>
      )} />
    ) : (
      <div className="register-form">
        <p>Log in your Garms account</p>
        <TextField hintText="Your e-mail"
          floatingLabelText="Input your e-mail address:"
          name="email"
          onChange={this.handleChange.bind(this)}
        />
        <TextField hintText="Password"
          floatingLabelText="Your password:"
          type="password"
          name="pwd"
          onChange={this.handleChange.bind(this)}
        />
        <RaisedButton label="Log In"
          primary={true}
          onClick={this.handleSubmit}
        />
      </div>
    );

    return (
      <MuiThemeProvider>
        <div>
          {loginForm}
        </div>
      </MuiThemeProvider>
    );
  }
}

export default withCookies(Login);
