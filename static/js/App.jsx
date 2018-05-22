import React from 'react'
import Header from './Header'
import Main from './Main'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
require('../css/garms.css');
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';

class App extends React.Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };

  constructor(props) {
    super(props);
    const { cookies } = this.props;
    this.state = {
      isAuth: cookies.get('isAuth')
    };
    this.handleLoginChange = this.handleLoginChange.bind(this);
    this.handleLoginSubmit = this.handleLoginSubmit.bind(this);
  }

  componentWillMount() {
  }

  componentDidMount(){
    const { cookies } = this.props;
    // console.log('Updating state')
    this.setState({ isAuth: cookies.get('isAuth') });
  }

  // Updates input field state
  handleLoginChange(event) {
    let value =  event.target.value;
    let name = event.target.name;
    this.setState({
      [name]: value
    });
  }

  // Asks the API if submitted pwd is correct and loggs the user in if yes
  handleLoginSubmit = (event) => {
    event.preventDefault();
    let email = this.state.email;
    let pwd = this.state.pwd;
    var auth = this.state.isAuth;
    const { cookies } = this.props;

    fetch(window.location.origin + '/api/login', {
      method: 'post',
      body: JSON.stringify({email: email, pwd: pwd})
    }).then(response => response.json())
      .then(data => {
        cookies.set('isAuth', data, { path: '/' });
        this.setState({ isAuth: data });
        return
      });
  }

  render() {
    // console.log(this.state);
    const body = this.state.isAuth == true || this.state.isAuth == "true" ? (
      <Main isAuth={this.state.isAuth} />
    ) : (
        <div className="register-form">
          <p>Log in your Garms account</p>
          <TextField hintText="Your e-mail"
            floatingLabelText="Input your e-mail address:"
            name="email"
            onChange={this.handleLoginChange}
          />
          <TextField hintText="Password"
            floatingLabelText="Your password:"
            type="password"
            name="pwd"
            onChange={this.handleLoginChange}
          />
          <RaisedButton label="Log In"
            primary={true}
            onClick={this.handleLoginSubmit}
          />
        </div>
    );

    return (
        <MuiThemeProvider>
          <div>
              <Header isAuth={this.state.isAuth} />
            <div className="content-wrapper">
              {body}
            </div>
          </div>
        </MuiThemeProvider>
    )
  }
}

// export default App;
export default withCookies(App);
