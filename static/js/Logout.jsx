// Register.jsx
import React from "react";

require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {withCookies, Cookies} from 'react-cookie';
import {instanceOf} from 'prop-types';


class Logout extends React.Component {
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };

    constructor(props) {
        super(props);
        const {cookies} = this.props;
        this.state = {
            isAuth: cookies.get('isAuth'),
            email: '',
            pwd: ''
        };
        this.handleLogout = this.handleLogout.bind(this);
    }

    handleLogout(event) {
        // alert('A name was submitted: ' + this.state.value);
        event.preventDefault();
        const {cookies} = this.props;

        console.log('Logging out', cookies);
        this.setState({
            isAuth: false
        });
        cookies.set('isAuth', false, {path: '/'});
        cookies.set('email', '', {path: '/'});
        cookies.set('sex', '', {path: '/'});
        cookies.set('username', '', {path: '/'});
        document.location.href="/";
    }

    render() {
        const logOutTile = this.state.isAuth == true || this.state.isAuth == "true" ? (
            <div className="register-form">
                <p>Log out from Garms</p>
                <RaisedButton label="Log Out"
                              primary={true}
                              onClick={this.handleLogout}
                />
            </div>
        ) : (
            <div className="register-form">
                <p>Thank you for being part of fashion revolution!</p>
            </div>
        );

        return (
            <MuiThemeProvider>
                <div>
                    {logOutTile}
                </div>
            </MuiThemeProvider>
        );
    }
}

export default withCookies(Logout);
