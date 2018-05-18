import React from "react";
// import { Button, Grid, Row, Col } from "react-bootstrap";
require('../css/garms.css');
import RaisedButton from 'material-ui/RaisedButton';
import { Link } from 'react-router-dom';
import { Route } from 'react-router-dom'

class Header extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    const button = this.props.isAuth == true || this.props.isAuth == "true" ? (
      <Route render={({ history }) => (
        <RaisedButton className="home-button" label="Log Out" onClick={() => { history.push('/logout') }} />
      )} />
    ) : (
      <Route render={({ history }) => (
        <RaisedButton className="home-button" label="Log In" onClick={() => { history.push('/login') }} />
      )} />
    );

    return (
      <div className="header-bar">
        <div className="logo" ><h1><Link style={{textDecoration: 'none'}} to="/">Garms</Link></h1></div>
        {button}
      </div>
    )
  }
}

export default Header;
