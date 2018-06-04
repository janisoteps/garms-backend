// TextSearch.jsx
import React from "react";
require('../css/garms.css');
require('../css/ball-atom.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import TextField from 'material-ui/TextField';
import Paper from 'material-ui/Paper';
import RaisedButton from 'material-ui/RaisedButton';
import ProductResults from './ProductResults';

//Component to search for products using text input
class TextSearch extends React.Component  {

    constructor(props) {
        super(props);
        // console.log('constructor sex: ', this.props.sex);

        this.state = {
            isAuth: this.props.isAuth,
            sex: this.props.sex,
            email: this.props.email,
            pwd: '',
            files: [],
            results: [],
            colors: {},
            mainColor: '',
            mainColorNr: 1,
            cats: [],
            mainCat: '',
            searchString: '',
            noResult: false,
            sexPickerWidth: '56px'
        };

        this.similarImageSearch = this.similarImageSearch.bind(this);
        this.textImageSearch = this.textImageSearch.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.onEnterPress = this.onEnterPress.bind(this);
        this.changeSex = this.changeSex.bind(this);
        this.changeSex = this.changeSex.bind(this);
        this.expandSexSelector = this.expandSexSelector.bind(this);
    }

    //Handle text input change
    handleChange(event) {
        let value =  event.target.value;
        let name = event.target.name;
        this.setState({
            [name]: value
        });
    }

    onEnterPress = (e) => {
        if(e.keyCode === 13 && e.shiftKey === false) {
            e.preventDefault();
            this.textImageSearch();
        }
    };

    // Sends similar product search request to server if user clicks on magnifying glass button
    // Updates results state with the response
    similarImageSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id){

        console.log('Similar image search launched');
        this.setState({
            loading: true
        });

        // let mainColor = color_1.toString().replace(/\s+/g, '');
        // let mainColor = this.state.mainColor;
        let siam_64 = siamese_64.toString().replace(/\s+/g, '');

        let mainCat = this.state.mainCat;
        if(mainCat.length === 0 || typeof mainCat === "undefined"){
            mainCat = img_cat_sc_txt;
        }

        console.log('Main cat: ', mainCat, ' , Img cat sc txt: ', img_cat_sc_txt);

        let searchString = window.location.origin + '/api/search?nr1_cat_ai=' + nr1_cat_ai
            + '&main_cat=' + mainCat
            + '&nr1_cat_sc=' + nr1_cat_sc
            + '&color_1=[' + color_1
            + ']&siamese_64=[' + siam_64
            + ']&sex=' + this.state.sex
            + '&id=' + prod_id;

        // console.log('search string: ', searchString);

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

    // Send request to server based on input string and set the response in state
    textImageSearch(){
        this.setState({
            loading: true
        });

        let inputString = this.state.searchString;
        if(inputString.length === 0){
            this.setState({
                loading: false,
                noResult: true
            });
            return
        }
        // console.log(inputString);
        let inputArray = inputString.split();
        // console.log(inputArray);
        let searchString = '';
        inputArray.forEach(word => searchString += '+' + word);

        console.log('String search with: ', searchString);
        fetch(window.location.origin + '/api/text?string=' + searchString + '&sex=' + this.state.sex, {
            method: 'get'
        }).then(function(response) { return response.json(); })
            .then(data => {
                console.log('Response: ', data);
                if (typeof data.res === "undefined") {
                    this.setState({
                        results: [],
                        loading: false,
                        noResult: true
                    });
                } else {
                    this.setState({
                        results: data.res,
                        mainCat: data.mainCat,
                        loading: false
                    });
                }
            });
    }

    changeSex(sex){
        this.props.changeSex(sex);
        this.setState({
            sex: sex
        });
        // this.expandSexSelector();
    }

    expandSexSelector(){
        let currentWidth = this.state.sexPickerWidth;

        console.log('Expanding sex selector ', currentWidth);
        if(currentWidth === '56px'){
            this.setState({
                sexPickerWidth: '270px'
            });
        } else {
            this.setState({
                sexPickerWidth: '56px'
            });
        }
    }


    // ------------------------ MAIN RENDER FUNCTION ----------------------------
    render () {
        // Render a spinner if loading state is true
        let Spinner = () => {
            return(
                <div>
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
            )
        };

        let NoResults = () => {
            return(
                <div>
                    {(this.state.noResult === true) && (
                        <div className="overlay">
                            <Paper zDepth={1} className="error-modal">
                                <h3>Couldn't find anything, try a different search</h3>
                                <RaisedButton className="ok-button" label="OK" onClick={() => { window.location.reload(); }} />
                            </Paper>
                        </div>
                    )}
                </div>
            )
        };

        let SearchBox = (
                <div className="text-search-box">
                    <div className="inner-text-search-box">
                        <TextField className="text-search-input"
                                   hintText="Purple denim jeans or..."
                                   floatingLabelText="What's your outfit idea?"
                                   name="searchString"
                                   onChange={this.handleChange.bind(this)}
                                   onKeyDown={this.onEnterPress}
                        />
                        <div className="text-search-button" onClick={this.textImageSearch}>
                            <div className="search-icon" />
                            <div className="search-text"> search</div>
                        </div>
                    </div>
                </div>
        );

        let SexSelector = () => {
            let sexPickerStyle = {
                position: 'fixed',
                right: '0',
                top: '70px',
                overflow: 'hidden',
                transition: 'width 300ms ease-in-out',
                width: this.state.sexPickerWidth,
                height: '56px',
                backgroundColor: '#FFFFFF',
                borderRadius: '28px 0px 0px 28px',
                boxShadow: '1px 1px 3px 0 rgba(0, 0, 0, 0.4)'
            };

            let selectorHiderStyle = {
                position: 'fixed',
                right: '0',
                top: '70px',
                overflow: 'hidden',
                transition: 'width 300ms ease-in-out',
                width: '56px',
                height: '56px',
                backgroundColor: '#FFFFFF',
                borderRadius: '28px 0px 0px 28px'
            };

            let sexOptionStyle1 = {
                display: 'inline-block',
                lineHeight: '33px',
                height: '56px',
                verticalAlign: 'middle',
                borderRadius: '28px',
                cursor: 'pointer',
                padding: this.state.sex !== 'women' ? '10px' : '5px',
                borderWidth: this.state.sex === 'women' && '5px',
                borderColor: this.state.sex === 'women' && '#7f649c',
                borderStyle: this.state.sex === 'women' && 'solid'
            };

            let sexOptionStyle2 = {
                display: 'inline-block',
                lineHeight: '33px',
                height: '56px',
                verticalAlign: 'middle',
                borderRadius: '28px',
                cursor: 'pointer',
                padding: this.state.sex !== 'men' ? '10px' : '5px',
                borderWidth: this.state.sex === 'men' && '5px',
                borderColor: this.state.sex === 'men' && '#7f649c',
                borderStyle: this.state.sex === 'men' && 'solid'
            };

            let sexOptionStyle3 = {
                display: 'inline-block',
                lineHeight: '33px',
                height: '56px',
                verticalAlign: 'middle',
                borderRadius: '28px',
                cursor: 'pointer',
                padding: this.state.sex !== '' ? '10px' : '5px',
                borderWidth: this.state.sex === '' && '5px',
                borderColor: this.state.sex === '' && '#7f649c',
                borderStyle: this.state.sex === '' && 'solid'
            };

            console.log('Image search sex: ', this.state.sex);

            return(
                <div>
                    <div style={sexPickerStyle}>
                        <div style={sexOptionStyle1} onClick={() => {this.changeSex('women')}}>women</div>
                        <div style={sexOptionStyle2} onClick={() => {this.changeSex('men')}}>men</div>
                        <div style={sexOptionStyle3} onClick={() => {this.changeSex('')}}>both</div>
                    </div>
                    <div style={selectorHiderStyle}></div>
                    <div className="sex-selector" onClick={this.expandSexSelector}></div>
                </div>
            )
        };

        let CatSelector = () => {

            return(
                <div className="cat-selector"></div>
            )
        };

        return(
            <MuiThemeProvider>
                <div>
                    <Spinner />
                    <NoResults />

                    {
                        this.state.results.length > 0 ? (
                            <ProductResults email={this.state.email} simImgSearch={(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id) => { this.similarImageSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id) }} results={this.state.results}/>
                        ) : (
                            SearchBox
                        )
                    }

                    <SexSelector />

                    <CatSelector />
                </div>
            </MuiThemeProvider>
        )
    }
}

export default TextSearch;
