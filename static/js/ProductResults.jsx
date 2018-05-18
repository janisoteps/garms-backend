// ProductResults.jsxx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Paper from 'material-ui/Paper';
// import { withCookies, Cookies } from 'react-cookie';
// import { instanceOf } from 'prop-types';
// import { Route } from 'react-router-dom';
// import Dropzone from 'react-dropzone';
// const pica = require('pica')();

class ProductResults extends React.Component  {
    // static propTypes = {
    //     cookies: instanceOf(Cookies).isRequired
    // };

    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render () {
        let tiles = this.props.results.map(product => {
            let productInfo = product[0];
            let brand = productInfo.brand;
            let color_1 = productInfo.color_1;
            let color_1_hex = productInfo.color_1_hex;
            let color_2 = productInfo.color_2;
            let color_2_hex = productInfo.color_2_hex;
            let id = productInfo.id;
            let img_cats_ai = productInfo.img_cats_ai;
            let nr1_cat_ai = productInfo.nr1_cat_ai;
            let img_url = productInfo.img_url;
            let name = productInfo.name;
            let currency = productInfo.currency;
            let price = productInfo.price.toFixed(2);
            let prod_url = productInfo.prod_url;
            let sale = productInfo.sale;
            let saleprice = productInfo.saleprice.toFixed(2);
            let shop = productInfo.shop;
            let siamese_64 = productInfo.siamese_64;

            return (
                <Paper zDepth={1} className="product-tile" key={id}>
                    <div className="product-name">{name}</div>
                    <div className="product-brand"><p>{brand} from {shop}</p></div>
                    <div className="product-image"><img src={img_url} /></div>
                    <div className={sale ? 'product-price-sale' : 'product-price'}>{sale ? currency+saleprice+', was '+currency+price : currency+price}</div>
                </Paper>
            );
        });

        return (
            <MuiThemeProvider>
                <div className="result-pane">
                    {tiles}
                </div>
            </MuiThemeProvider>
        );
    }
}

export default ProductResults;
