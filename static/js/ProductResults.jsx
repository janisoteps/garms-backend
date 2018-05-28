// ProductResults.jsxx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Paper from 'material-ui/Paper';


class ProductResults extends React.Component  {
    constructor(props) {
        super(props);
        this.simImSrc = this.simImSrc.bind(this);
    }

    simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64){
        this.props.simImgSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64);
    }

    render () {
        let tiles = this.props.results.map(product => {
            // console.log('Product data passed to result list: ', product[0]);
            let productInfo = product[0];
            let brand = productInfo.brand;
            let color_1 = productInfo.color_1;
            let color_1_hex = productInfo.color_1_hex;
            let color_2 = productInfo.color_2;
            let color_2_hex = productInfo.color_2_hex;
            let color_3 = productInfo.color_3;
            let color_3_hex = productInfo.color_3_hex;
            let id = productInfo.id;
            let img_cat_sc_txt = productInfo.img_cats_sc_txt[productInfo.img_cats_sc_txt.length - 1];
            let nr1_cat_ai = productInfo.nr1_cat_ai;
            let nr1_cat_sc = productInfo.nr1_cat_sc;
            let img_url = productInfo.img_url;
            let name = productInfo.name;
            let currency = productInfo.currency;
            let price = productInfo.price.toFixed(2);
            // let prod_url = productInfo.prod_url;
            let sale = productInfo.sale;
            let saleprice = productInfo.saleprice.toFixed(2);
            let shop = productInfo.shop;
            let siamese_64 = productInfo.siamese_64;

            // nr1_cat_ai, nr1_cat_sc, color_1, siamese_64

            // Dynamic CSS for image color choice modal
            if(color_1_hex.length > 0){
                var colorStyle1 = {
                    width: '70px',
                    height: '70px',
                    borderRadius: '30px',
                    backgroundColor: color_1_hex,
                    margin: '10px',
                    display: 'inline-block',
                    cursor: 'pointer'
                };
                var colorStyle2 = {
                    width: '70px',
                    height: '70px',
                    borderRadius: '30px',
                    backgroundColor: color_2_hex,
                    margin: '10px',
                    display: 'inline-block',
                    cursor: 'pointer'
                };
                var colorStyle3 = {
                    width: '70px',
                    height: '70px',
                    borderRadius: '30px',
                    backgroundColor: color_3_hex,
                    margin: '10px',
                    display: 'inline-block',
                    cursor: 'pointer'
                };
            }

            let ColorPicker = () => {
              return (
                  <div style={pickerStyle}></div>
              )
            };

            return (
                <Paper zDepth={1} className="product-tile" key={id}>
                    <div className="product-name">{name}</div>
                    <div className="product-brand"><p>{brand} from {shop}</p></div>
                    <img className="product-image" src={img_url} />
                    <div className={sale ? 'product-price-sale' : 'product-price'}>{sale ? currency+saleprice+', was '+currency+price : currency+price}</div>
                    <div className="add-to-favorites" ></div>
                    <div className="search-similar" onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64); }}></div>
                    <div className="color-picker"></div>
                    {/*onClick={(nr1_cat_ai, nr1_cat_sc, color_1, siamese_64) => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, color_1, siamese_64); }}*/}
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
