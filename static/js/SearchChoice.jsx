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
                <div>
                    <div className="search-choice">
                        <Route render={({ history }) => (
                            <div
                                className="search-choice-button"
                                onClick={() => { history.push('/imagesearch') }}>
                                <div className="search-choice-title">
                                    <div className="image-search-icon"></div>
                                    <div className="search-choice-text">Search from photo</div>
                                </div>
                            </div>
                        )} />

                        <Route render={({ history }) => (
                            <div
                                className="search-choice-button"
                                onClick={() => { history.push('/textsearch') }}>
                                <div className="search-choice-title">
                                    <div className="text-search-icon"></div>
                                    <div className="search-choice-text">Type your search</div>
                                </div>
                            </div>
                        )} />
                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}

export default SearchChoice;

