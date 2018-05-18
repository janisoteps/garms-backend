import React from "react";
import RaisedButton from 'material-ui/FlatButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { Route } from 'react-router-dom';


class SearchChoice extends React.Component {
    constructor(props) {
        super(props);

    }



    render () {

        return (
            <MuiThemeProvider>
                <div className="search-choice">
                    <Route render={({ history }) => (
                        <RaisedButton className="home-button" label="Take / Upload Photo" onClick={() => { history.push('/imagesearch') }} />
                    )} />
                    <Route render={({ history }) => (
                        <RaisedButton className="home-button" label="Type Your Search" onClick={() => { history.push('/textsearch') }} />
                    )} />
                </div>
            </MuiThemeProvider>
        )
    }
}

export default SearchChoice;
