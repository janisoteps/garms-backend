import React from "react";
import RaisedButton from 'material-ui/FlatButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { Route } from 'react-router-dom';
import Paper from 'material-ui/Paper';


class SearchChoice extends React.Component {
    constructor(props) {
        super(props);

    }



    render () {

        return (
            <MuiThemeProvider>
                <div className="search-choice">
                    <Route render={({ history }) => (
                        <Paper style={{
                            height: '20vh',
                            width: '80vw',
                            maxWidth: '600px',
                            backgroundColor: '#7c5e93',
                            color: 'white',
                            display: 'inline-block',
                            paddingTop: 'calc(10vh - 20px)',
                            cursor: 'pointer'
                        }} zDepth={2} onClick={() => { history.push('/imagesearch') }}>
                            <h2>Take / Upload Photo</h2>
                        </Paper>
                    )} />
                </div>
                <div className="search-choice">
                    <Route render={({ history }) => (
                        <Paper style={{
                            height: '20vh',
                            width: '80vw',
                            maxWidth: '600px',
                            backgroundColor: '#5f5d92',
                            color: 'white',
                            display: 'inline-block',
                            paddingTop: 'calc(10vh - 20px)',
                            cursor: 'pointer'
                        }} zDepth={2} onClick={() => { history.push('/textsearch') }}>
                            <h2>Type Your Search</h2>
                        </Paper>
                    )} />
                </div>
            </MuiThemeProvider>
        )
    }
}

export default SearchChoice;


{/*<RaisedButton buttonStyle={{height: '70px'}} fullWidth={true} primary={true} className="home-button" label="Take / Upload Photo" onClick={() => { history.push('/imagesearch') }} />*/}
