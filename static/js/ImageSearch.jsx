// ImageSearch.jsx
import React from "react";
require('../css/garms.css');
require('../css/ball-atom.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Route } from 'react-router-dom';
import Dropzone from 'react-dropzone';
// const pica = require('pica')();
import ProductResults from './ProductResults';
import Paper from 'material-ui/Paper';
import RaisedButton from 'material-ui/RaisedButton';


class ImageSearch extends React.Component  {
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };

    constructor(props) {
        super(props);
        const { cookies } = this.props;
        this.state = {
            isAuth: cookies.get('isAuth'),
            email: '',
            pwd: '',
            files: [],
            results: [],
            colors: {}
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.onDrop = this.onDrop.bind(this);
        this.getColors = this.getColors.bind(this);
        this.colorImageSearch = this.colorImageSearch.bind(this);
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

    onDrop(acceptedFiles, rejectedFiles) {
        this.setState({
            files: acceptedFiles
        });
    }

    // doSearch(){
    //     let imageFile = this.state.files[0];
    //
    //     const data = new FormData();
    //     data.append('image', imageFile);
    //
    //     fetch(window.location.origin + '/api/image', {
    //         method: 'post',
    //         body: data
    //     }).then(response => {
    //         return response.json();
    //     }).then(data => {
    //         console.log(data);
    //         this.setState({
    //             results: data.res
    //         });
    //     });
    // }

    getColors(){
        this.setState({
            loading: true
        });

        let imageFile = this.state.files[0];

        let data = new FormData();
        data.append('image', imageFile);

        fetch(window.location.origin + '/api/color', {
            method: 'post',
            body: data
        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
            this.setState({
                colors: data.res,
                loading: false
            });
        });
    }

    colorImageSearch(colorNr){
        let imageFile = this.state.files[0];
        let color_data = new FormData();
        color_data.append('image', imageFile);

        let colorName = 'color_' + colorNr;
        let colorValue = this.state.colors[colorName].toString().replace(/\s+/g, '');
        color_data.append('color', colorValue);

        this.setState({
            colors: {},
            loading: true
        });

        fetch(window.location.origin + '/api/colorimage', {
            method: 'post',
            body: color_data
        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
            this.setState({
                results: data.res,
                loading: false
            });

        });
    }

    render () {

        let preview = this.state.files.length > 0 ? (
            <div className="preview-container">
                <img className="image-preview" src={this.state.files[0].preview} />
                <div className="search-button" onClick={this.getColors}><p>search</p></div>
            </div>
        ) : (
            <p> </p>
        );
        console.log(this.state.files);
        // var setLoginState = this.props.setLoginState;
        // console.log('Login file isAuth', this.state.isAuth);
        let searchForm = this.state.isAuth === true || this.state.isAuth == "true" ? (
            <div>
                {preview}
                <section>
                    <div className="dropzone">
                        <Dropzone className="image-dropzone" onDrop={(files) => this.onDrop(files)} accept="image/jpeg">
                            <p>Drop image here or click to select image to upload.</p>
                        </Dropzone>
                    </div>
                    <aside>
                        <ul>
                            {
                                this.state.files.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                            }
                        </ul>
                    </aside>
                </section>
            </div>
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

        if(this.state.results){
            var searchOrResults = this.state.results.length > 0 ? (
                <ProductResults results={this.state.results}/>
            ) : (
                searchForm
            );
        } else {
            searchOrResults = (
                <div className="overlay">
                    <Paper zDepth={1} className="color-modal">
                        <h3>Can't recognize the outfit, try a better quality photo</h3>
                        <RaisedButton className="ok-button" label="OK" onClick={() => { window.location.reload(); }} />
                    </Paper>
                </div>
            )
        }


        if(Object.keys(this.state.colors).length > 0){
            var colorStyle1 = {
                width: '70px',
                height: '70px',
                borderRadius: '30px',
                backgroundColor: this.state.colors.color_1_hex,
                margin: '10px',
                display: 'inline-block',
                cursor: 'pointer'
            };
            var colorStyle2 = {
                width: '70px',
                height: '70px',
                borderRadius: '30px',
                backgroundColor: this.state.colors.color_2_hex,
                margin: '10px',
                display: 'inline-block',
                cursor: 'pointer'
            };
            var colorStyle3 = {
                width: '70px',
                height: '70px',
                borderRadius: '30px',
                backgroundColor: this.state.colors.color_3_hex,
                margin: '10px',
                display: 'inline-block',
                cursor: 'pointer'
            };
        }

        return (
            <MuiThemeProvider>
                <div>
                    {searchOrResults}

                    {(Object.keys(this.state.colors).length > 0) && (
                        <div className="overlay">
                            <Paper zDepth={1} className="color-modal">
                                <p>I found these colors in your photo, choose which one to search for:</p>
                                <div style={colorStyle1} onClick={() => this.colorImageSearch(1)} />
                                <div style={colorStyle2} onClick={() => this.colorImageSearch(2)} />
                                <div style={colorStyle3} onClick={() => this.colorImageSearch(3)} />
                            </Paper>
                        </div>
                    )}

                    {(this.state.loading === true) && (
                        <div className="overlay">
                            <div className="la-ball-atom la-3x">
                                <div />
                                <div />
                                <div />
                                <div />
                            </div>
                        </div>
                    )}
                </div>
            </MuiThemeProvider>
        );
    }
}

export default withCookies(ImageSearch);
