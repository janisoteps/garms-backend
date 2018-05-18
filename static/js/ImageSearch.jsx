// ImageSearch.jsx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
// import { Route } from 'react-router-dom';
import Dropzone from 'react-dropzone';
// const pica = require('pica')();
import ProductResults from './ProductResults';

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
            results: []
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.onDrop = this.onDrop.bind(this);
        this.doSearch = this.doSearch.bind(this);
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

    doSearch(){
        let imageFile = this.state.files[0];

        const data = new FormData();
        data.append('image', imageFile);

        fetch(window.location.origin + '/api/image', {
            method: 'post',
            body: data
        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
            this.setState({
                results: data.res
            });
        });
    }

    render () {

        let preview = this.state.files.length > 0 ? (
            <div className="preview-container">
                <img className="image-preview" src={this.state.files[0].preview} />
                <div className="search-button" onClick={this.doSearch}><p>search</p></div>
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
                        <Dropzone className="image-dropzone" onDrop={(files) => this.onDrop(files)} accept="image/jpeg, image/png">
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

        let searchOrResults = this.state.results.length > 0 ? (
            <ProductResults results={this.state.results}/>
        ) : (
            searchForm
        );

        // let searchBody =

        return (
            <MuiThemeProvider>
                <div>
                    {searchOrResults}
                </div>
            </MuiThemeProvider>
        );
    }
}

export default withCookies(ImageSearch);
