// Profile.jsx
import React from "react";
require('../css/garms.css');
import {Route} from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Paper from 'material-ui/Paper';

class Profile extends React.Component  {
    constructor(props) {
        super(props);
        this.state = {
            isAuth: this.props.isAuth,
            username: this.props.username,
            email: this.props.email,
            favorites: []
        };
    }

    componentDidMount() {
        let searchString = window.location.origin + '/api/favorites?email=' + this.state.email;

        fetch(searchString, {
            method: 'get',
        }).then(function(response) {
            return response.json();
        }).then(data => {
            // let favData = JSON.parse(data.res);
            console.log(data.res);
            this.setState({
                favorites: data.res,
            });
        });
    }

    render () {
        const logOutButton = this.state.isAuth === "true" ? (
            <Route render={({ history }) => (
                <RaisedButton className="login-button" label="Log Out" onClick={() => { history.push('/logout') }} />
            )} />
        ) : (
            <Route render={({ history }) => (
                <RaisedButton className="login-button" label="Log In" onClick={() => { history.push('/login') }} />
            )} />
        );

        let greetingStyle = {
            textAlign: 'center',
            marginTop: '70px'
        };

        let favTiles = this.state.favorites.map(product => {
            // console.log('Product data passed to result list: ', product[0]);
            let productInfo = product[0];
            // let img_hash = productInfo.img_hash;
            let brand = productInfo.brand;
            // let color_1 = productInfo.color_1;
            // let color_1_hex = productInfo.color_1_hex;
            // let color_2 = productInfo.color_2;
            // let color_2_hex = productInfo.color_2_hex;
            // let color_3 = productInfo.color_3;
            // let color_3_hex = productInfo.color_3_hex;
            let id = productInfo.id;
            // let img_cat_sc_txt = productInfo.img_cats_sc_txt[productInfo.img_cats_sc_txt.length - 1];
            // let nr1_cat_ai = productInfo.nr1_cat_ai;
            // let nr1_cat_sc = productInfo.nr1_cat_sc;
            let img_url = productInfo.img_url;
            let name = productInfo.name;
            let currency = productInfo.currency;
            let price = productInfo.price.toFixed(2);
            let prod_url = productInfo.prod_url;
            let sale = productInfo.sale;
            let saleprice = productInfo.saleprice.toFixed(2);
            let shop = productInfo.shop;
            // let siamese_64 = productInfo.siamese_64;

            return (
                <Paper zDepth={1} className="product-tile" key={id}>
                    <div className="product-name">{name}</div>
                    <div className="product-brand"><p>{brand} from {shop}</p></div>
                    <img className="product-image" src={img_url} />
                    <div className={sale ? 'product-price-sale' : 'product-price'}>{sale ? currency+saleprice+', was '+currency+price : currency+price}</div>
                    <a href={prod_url} target="_blank"> <h5>Go to product shop page</h5></a>
                    {/*<div style={faveDrawerStyle} >Added to faves</div>*/}
                    {/*<div className="add-to-favorites" onClick={() => { this.addToFavs(img_hash); }}></div>*/}
                    {/*<div className="search-similar" onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64); }}></div>*/}
                    {/*<ColorPicker/>*/}
                </Paper>
            )
        });


        let favoritesList = this.state.favorites.length > 0 ? (
            favTiles
        ) : (
            <h2> You haven't added any products to your favorites yet</h2>
        );

        return (
            <MuiThemeProvider>
                <div className="profile-product-list">
                    <h2 style={greetingStyle}>Hi {this.state.username}!</h2>
                    <h4>Below you will find items added to your faves</h4>
                    <br></br>
                    <div className="result-pane">
                        {favoritesList}
                    </div>
                    <br></br>
                    {logOutButton}
                </div>
            </MuiThemeProvider>
        )
    }
}

export default Profile;