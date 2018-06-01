import React from "react";
// import { Button, Grid, Row, Col } from "react-bootstrap";
require('../css/garms.css');
// import RaisedButton from 'material-ui/RaisedButton';
import {Link} from 'react-router-dom';
import {Route} from 'react-router-dom';

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isAuth: this.props.isAuth
        };
    }

    render() {
        // console.log('header state: ', this.state);
        const buttons = this.state.isAuth == "true" ? (
            <div>
                <Route render={({history}) => (
                    <div className="home-button" onClick={() => {
                        history.push('/')
                    }}>
                    </div>
                )}/>
                <Route render={({history}) => (
                    <div className="profile-button" onClick={() => {
                        history.push('/profile')
                    }}>
                    </div>
                )}/>
                <Route render={({history}) => (
                    <div className="favorites-button" onClick={() => {
                        history.push('/profile')
                    }}>
                    </div>
                )}/>
            </div>
        ) : (
            <p className="header-prompt">Lets go shopping!</p>
        );

        return (
            <div className="header-bar">
                <div className="logo"><h1><Link style={{textDecoration: 'none', color: '#5f5d92'}} to="/">Garms</Link>
                </h1></div>
                {buttons}
            </div>
        )
    }
}

export default Header;
