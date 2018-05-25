import React from 'react'
import { Switch, Route } from 'react-router-dom'
// import TestList from './TestList'
import Register from './Register'
import Login from './Login'
import Logout from './Logout'
import SearchChoice from './SearchChoice'
import ImageSearch from './ImageSearch'
import TextSearch from './TextSearch'


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
        console.log('Main isAuth: ',this.props);
        return (
            <main>
                <Switch>
                    <Route exact path='/' component={SearchChoice} />
                    <Route path='/register' component={Register} />
                    <Route path='/login' isAuth={this.props} component={Login} />
                    <Route path='/logout' isAuth={this.props.isAuth} component={Logout} />
                    <Route path='/imagesearch' component={ImageSearch} />
                    <Route path='/textsearch' isAuth={this.props.isAuth} component={TextSearch} />
                </Switch>
            </main>
        )
    }
}

export default Main;
