import React from 'react'
import { Switch, Route } from 'react-router-dom'
// import TestList from './TestList'
import Register from './Register'
import Login from './Login'
import Logout from './Logout'
import SearchChoice from './SearchChoice'
import ImageSearch from './ImageSearch'
import TextSearch from './TextSearch'
import Profile from './Profile'


// The Main component renders one of the provided
// Routes (provided that one matches). The / route will only match
// when the pathname is exactly the string "/"

class Main extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
    }

    render() {
        // console.log('Main isAuth: ',this.props.isAuth);
        // console.log('Main sex: ',this.props.sex);
        // console.log('Main email: ', this.props.email);
        console.log('Main username: ', this.props.username);
        return (
            <main>
                <Switch>
                    <Route exact path='/' component={SearchChoice} />
                    <Route path='/register' component={Register} />
                    <Route path='/login' component={Login} />
                    <Route path='/logout' component={Logout} />
                    <Route path='/imagesearch' render={(props) => <ImageSearch
                        {...props}
                        sex={this.props.sex}
                        isAuth={this.props.isAuth}
                        email={this.props.email}
                        />}
                    />
                    <Route path='/textsearch'
                           render={(props) => <TextSearch
                           {...props} sex={this.props.sex}
                           isAuth={this.props.isAuth}
                           email={this.props.email}
                        />}
                    />
                    <Route path='/profile'
                           render={(props) => <Profile
                               {...props}
                               username={this.props.username}
                               sex={this.props.sex}
                               isAuth={this.props.isAuth}
                               email={this.props.email}
                           />}
                    />
                </Switch>
            </main>
        )
    }
}

export default Main;
