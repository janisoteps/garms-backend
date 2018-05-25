// ImageSearch.jsx
import React from "react";
require('../css/garms.css');
require('../css/ball-atom.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
// import { Route } from 'react-router-dom';
import Dropzone from 'react-dropzone';
// const pica = require('pica')();
import ProductResults from './ProductResults';
import Paper from 'material-ui/Paper';
import RaisedButton from 'material-ui/RaisedButton';


//Component to search for products using an uploaded image
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
            colors: {},
            mainColor: '',
            mainColorNr: 1,
            cats: [],
            mainCat: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.onDrop = this.onDrop.bind(this);
        this.getColors = this.getColors.bind(this);
        this.colorImageSearch = this.colorImageSearch.bind(this);
        this.similarImageSearch = this.similarImageSearch.bind(this);
        this.getColorsCats = this.getColorsCats.bind(this);
        this.colorCatImageSearch = this.colorCatImageSearch.bind(this);
        this.setColorCat = this.setColorCat.bind(this);
    }

    // Handles login input change
    handleChange(event) {
        let value =  event.target.value;
        let name = event.target.name;
        this.setState({
            [name]: value
        });
    }

    //Submits login request to server and sets state/cookies if successful
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

    // When file is uploaded adds the file to state from drop zone
    onDrop(acceptedFiles, rejectedFiles) {
        this.setState({
            files: acceptedFiles
        });
    }

    // Sends color extraction request to server, sets state to colors in response
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

    // Sends color and category prediction request to server, sets state to colors and categories in response
    getColorsCats(){
        this.setState({
            loading: true
        });

        let imageFile = this.state.files[0];

        let data = new FormData();
        data.append('image', imageFile);

        fetch(window.location.origin + '/api/colorcat', {
            method: 'post',
            body: data
        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
            this.setState({
                colors: data.res.colors,
                cats: data.res['img_cats_ai_txt'],
                mainCat: data.res['img_cats_ai_txt'][0],
                loading: false
            });
        });
    }

    // Once user has selected color from their image sends request to server to
    // analyse the image category and find the best color matches
    colorCatImageSearch(){
        // let colorCatData = new FormData();
        // color_data.append('image', imageFile);

        let colorName = 'color_' + this.state.mainColor;
        let colorValue = this.state.colors[colorName].toString().replace(/\s+/g, '');
        // color_data.append('color', colorValue);

        let catName = this.state.mainCat;

        this.setState({
            colors: {},
            cats: [],
            files: [],
            loading: true,
            mainColor: colorValue
        });

        let searchString = window.location.origin + '/api/colorcatsearch?cat_ai_txt=' + catName + '&color_rgb=' + colorValue;

        fetch(searchString, {
            method: 'get'
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

    // Once user has selected color from their image sends request to server to
    // analyse the image category and find the best color matches
    colorImageSearch(colorNr){
        let imageFile = this.state.files[0];
        let color_data = new FormData();
        color_data.append('image', imageFile);

        let colorName = 'color_' + colorNr;
        let colorValue = this.state.colors[colorName].toString().replace(/\s+/g, '');
        color_data.append('color', colorValue);

        this.setState({
            colors: {},
            loading: true,
            mainColor: colorValue
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

    // Sends similar product search request to server if user clicks on magnifying glass button
    // Updates results state with the response
    similarImageSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64){

        console.log('Similar image search launched');
        this.setState({
            loading: true
        });

        let mainColor = color_1.toString().replace(/\s+/g, '');
        // let mainColor = this.state.mainColor;
        let siam_64 = siamese_64.toString().replace(/\s+/g, '');

        let searchString = window.location.origin + '/api/search?nr1_cat_ai=' + nr1_cat_ai + '&main_cat=' + this.state.mainCat + '&nr1_cat_sc=' + nr1_cat_sc + '&color_1=[' + mainColor + ']&siamese_64=[' + siam_64 + ']';

        console.log('search string: ', searchString);

        fetch(searchString, {
            method: 'get',
        }).then(function(response) {
            return response.json();
        }).then(data => {
                console.log(data);
                this.setState({
                    results: data.res,
                    loading: false
                });
                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });
                window.scrollTo(0, 0);
            });
    }

    // Set main color and category state based on selection from modal
    setColorCat(selection){
        if(selection['cat'].length > 0) {
            let mainCat = selection['cat'];
            this.setState({
                mainCat: mainCat
            });
        } else {
            let colorNr = selection['color'];
            this.setState({
                mainColor: colorNr
            });
        }
    }

    render () {

        // Element that shows preview of just uploaded photo
        let preview = this.state.files.length > 0 ? (
            <div className="preview-container">
                <img className="image-preview" src={this.state.files[0].preview} />
                <div className="search-button" onClick={this.getColorsCats}><p>search</p></div>
            </div>
        ) : (
            <p> </p>
        );

        // Shows either image drop zone or login form if not authorized
        let searchForm = this.state.isAuth === true || this.state.isAuth == "true" ? (
            <div>
                { this.state.files.length > 0 ? (
                        preview
                    ) : (
                        <section>
                            <div className="dropzone">
                                <Dropzone className="image-dropzone" onDrop={(files) => this.onDrop(files)} accept="image/jpeg">
                                    <div className="drop-text"><h1>Drop image here or click to select image to upload</h1></div>
                                </Dropzone>
                            </div>
                        </section>
                    )
                }
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

        // Nested logic: if results object is not falsy then show either product result component if state has results
        // Or show a response saying that image wasn't recognized
        //                 <ProductResults simImgSearch={() => { this.similarImageSearch() }} results={this.state.results}/>
        if(this.state.results){
            var searchOrResults = this.state.results.length > 0 ? (
                <ProductResults simImgSearch={(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64) => { this.similarImageSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64) }} results={this.state.results}/>
            ) : (
                searchForm
            );
        } else {
            searchOrResults = (
                <div className="overlay">
                    <Paper zDepth={1} className="error-modal">
                        <h3>Can't recognize the outfit, try a better quality photo</h3>
                        <RaisedButton className="ok-button" label="OK" onClick={() => { window.location.reload(); }} />
                    </Paper>
                </div>
            )
        }

        // Dynamic CSS for image color choice modal
        if(Object.keys(this.state.colors).length > 0){
            var colorStyle1 = {
                width: '70px',
                height: '70px',
                borderRadius: '30px',
                backgroundColor: this.state.colors.color_1_hex,
                margin: '10px',
                display: 'inline-block',
                cursor: 'pointer',
                borderWidth: this.state.mainColor === 1 && '5px',
                borderColor: this.state.mainColor === 1 && '#7f649c',
                borderStyle: this.state.mainColor === 1 && 'solid'
            };
            var colorStyle2 = {
                width: '70px',
                height: '70px',
                borderRadius: '30px',
                backgroundColor: this.state.colors.color_2_hex,
                margin: '10px',
                display: 'inline-block',
                cursor: 'pointer',
                borderWidth: this.state.mainColor === 2 && '5px',
                borderColor: this.state.mainColor === 2 && '#7f649c',
                borderStyle: this.state.mainColor === 2 && 'solid'
            };
            var colorStyle3 = {
                width: '70px',
                height: '70px',
                borderRadius: '30px',
                backgroundColor: this.state.colors.color_3_hex,
                margin: '10px',
                display: 'inline-block',
                cursor: 'pointer',
                borderWidth: this.state.mainColor === 3 && '5px',
                borderColor: this.state.mainColor === 3 && '#7f649c',
                borderStyle: this.state.mainColor === 3 && 'solid'
            };
        }

        // if colors are set in state show choice modal to select one main color
        // stateless component
        let ColorChoiceModal = () => {
            if(Object.keys(this.state.colors).length > 0){
                let cat1 = this.state.cats[0];
                let cat2 = this.state.cats[1];
                let cat3 = this.state.cats[2];

                let catClass = (cat) => {
                    if(this.state.mainCat === cat){
                        return 'cat-choice-main'
                    } else {
                        return 'cat-choice'
                    }
                };

                if(Object.keys(this.state.cats).length > 0){
                    return(
                        <div className="overlay">
                            <Paper zDepth={1} className="color-modal">
                                <h5>I found these colors and outfits in your photo</h5>
                                <p>choose which color to search for:</p>
                                <div style={colorStyle1} onClick={() => this.setColorCat({'color': 1, 'cat':''})} />
                                <div style={colorStyle2} onClick={() => this.setColorCat({'color': 2, 'cat':''})} />
                                <div style={colorStyle3} onClick={() => this.setColorCat({'color': 3, 'cat':''})} />
                                <p>choose which outfit type to search for:</p>
                                <div>
                                    <div className={catClass(cat1)} onClick={() => this.setColorCat({'cat': cat1})} >{cat1}</div>
                                    <div className={catClass(cat2)} onClick={() => this.setColorCat({'cat': cat2})} >{cat2}</div>
                                    <div className={catClass(cat3)} onClick={() => this.setColorCat({'cat': cat3})} >{cat3}</div>
                                </div>
                                <div className="colorcat-search-button" onClick={() => this.colorCatImageSearch() } >go</div>
                            </Paper>
                        </div>
                    )
                } else {
                    return(
                        <div className="overlay">
                            <Paper zDepth={1} className="color-modal">
                                <h3>Can't recognize the outfit, try a better quality photo</h3>
                                <RaisedButton className="ok-button" label="OK" onClick={() => { window.location.reload(); }} />
                            </Paper>
                        </div>
                    )
                }

            } else {
                return(
                    ''
                )
            }
        };

        // Main render
        return (
            <MuiThemeProvider>
                <div>
                    {searchOrResults}

                    <ColorChoiceModal />

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
