// ProductResults.jsxx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Paper from 'material-ui/Paper';


class ProductResults extends React.Component  {
    constructor(props) {
        super(props);
        this.simImSrc = this.simImSrc.bind(this);
        this.state = {
            pickerExpanded: 0
        };
        this.expandDrawer = this.expandDrawer.bind(this);
    }

    simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64){
        this.setState({
            pickerExpanded: 0
        });
        this.props.simImgSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64);
    }

    expandDrawer = (id, pickerId) => {
        console.log(id, ' vs ', pickerId);
        if (id === pickerId){
            this.setState({
                pickerExpanded: 0
            });
        } else {
            this.setState({
                pickerExpanded: id
            });
        }
    };

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
                    width: '50px',
                    height: '50px',
                    borderRadius: '25px',
                    backgroundColor: color_1_hex,
                    margin: '7px',
                    marginRight: '0px',
                    display: 'inline-block',
                    cursor: 'pointer'
                };
                var colorStyle2 = {
                    width: '50px',
                    height: '50px',
                    borderRadius: '25px',
                    backgroundColor: color_2_hex,
                    margin: '7px',
                    marginRight: '0px',
                    display: 'inline-block',
                    cursor: 'pointer'
                };
                var colorStyle3 = {
                    width: '50px',
                    height: '50px',
                    borderRadius: '25px',
                    backgroundColor: color_3_hex,
                    margin: '7px',
                    marginRight: '0px',
                    display: 'inline-block',
                    cursor: 'pointer'
                };
            }
            let rgbSum = eval(color_1.join('+'));

            var pickerBgUrl;

            if (rgbSum > 400) {
                pickerBgUrl = 'url("data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9JzIwMCcgd2lkdGg9JzIwMCcgIGZpbGw9IiMwMDAwMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHZlcnNpb249IjEuMSIgeD0iMHB4IiB5PSIwcHgiIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCAxMDAgMTAwOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+PHBhdGggZD0iTTk0LjksMTcuNmMtMC44LTUuNy00LTguNi02LjYtMTAuNWMtMi45LTIuMS02LjYtMi42LTkuOS0xLjNjLTMuNSwxLjMtNiwzLjktOC42LDYuNWMtMywzLjItNi4yLDYuMi05LjMsOS4zICBjLTMuMS0yLTQuOC0xLjgtNy4zLDAuNmMtMS41LDEuNS0zLDIuOS00LjQsNC40Yy0xLjUsMS42LTEuNyw0LjItMC4yLDUuOGMwLjcsMC44LDEuNywxLjMsMi43LDJjLTEuMSwwLjktMS42LDEuMy0yLDEuNyAgQzM4LDQ3LjQsMjYuNiw1OC44LDE1LjIsNzAuMWMtMi42LDIuNi00LjcsNS40LTUuNyw5LjFjLTAuNSwyLTEuNywzLjktMi44LDUuNmMtMC4yLDAuMy0wLjQsMC41LTAuNiwwLjhjLTEuNywyLjMtMS42LDUuNCwwLjQsNy40ICBjMC4xLDAuMSwwLjIsMC4yLDAuMiwwLjJjMiwyLDUsMi4xLDcuMywwLjVjMCwwLDAsMCwwLjEsMGMxLjctMS4yLDMuMy0yLjgsNS4yLTMuMWM0LjItMC45LDcuNS0zLDEwLjQtNkM0MS4zLDczLjQsNTIuNiw2Miw2NCw1MC43ICBjMC41LTAuNSwxLTAuOSwxLjgtMS43YzAuNSwwLjcsMC44LDEuMywxLjMsMS44YzIuMiwyLjMsNC42LDIuMiw2LjksMGMxLjItMS4yLDIuNC0yLjQsMy42LTMuNmMyLjktMi45LDMuNy00LjMsMS4xLTcuOCAgYzIuNC0yLjQsNC44LTQuNyw3LjItNy4xYzMuMy0zLjQsNy4yLTYuMyw4LjctMTEuMUM5NSwyMCw5NS4xLDE4LjgsOTQuOSwxNy42eiBNNjEuNiw0Ny4yQzQ5LjksNTguOSwzOC4yLDcwLjYsMjYuNSw4Mi4yICBjLTIuMiwyLjItNC43LDMuNi03LjcsNC40Yy0yLjMsMC42LTQuMywyLjItNi40LDMuM2MtMC4yLDAuMS0wLjQsMC4zLTAuNiwwLjRjLTAuNiwwLjUtMS41LDAuNC0yLTAuMWMwLDAsMCwwLDAsMCAgYy0wLjUtMC42LTAuNi0xLjQtMC4xLTJjMC43LTAuOSwxLjQtMS44LDItMi43YzAuOC0xLjMsMS41LTIuOCwxLjgtNC4zYzAuNi0yLjksMS45LTUuMywzLjktNy4zYzEyLjEtMTIuMSwyNC4yLTI0LjIsMzYuMS0zNi4xICBjMi45LDIuOCw1LjcsNS43LDguNyw4LjdDNjIuMiw0Ni41LDYxLjksNDYuOSw2MS42LDQ3LjJ6Ij48L3BhdGg+PC9zdmc+")';
            } else {
                pickerBgUrl = 'url("data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9JzIwMCcgd2lkdGg9JzIwMCcgIGZpbGw9IiNmZmZmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHZlcnNpb249IjEuMSIgeD0iMHB4IiB5PSIwcHgiIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCAxMDAgMTAwOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+PHBhdGggZD0iTTk0LjksMTcuNmMtMC44LTUuNy00LTguNi02LjYtMTAuNWMtMi45LTIuMS02LjYtMi42LTkuOS0xLjNjLTMuNSwxLjMtNiwzLjktOC42LDYuNWMtMywzLjItNi4yLDYuMi05LjMsOS4zICBjLTMuMS0yLTQuOC0xLjgtNy4zLDAuNmMtMS41LDEuNS0zLDIuOS00LjQsNC40Yy0xLjUsMS42LTEuNyw0LjItMC4yLDUuOGMwLjcsMC44LDEuNywxLjMsMi43LDJjLTEuMSwwLjktMS42LDEuMy0yLDEuNyAgQzM4LDQ3LjQsMjYuNiw1OC44LDE1LjIsNzAuMWMtMi42LDIuNi00LjcsNS40LTUuNyw5LjFjLTAuNSwyLTEuNywzLjktMi44LDUuNmMtMC4yLDAuMy0wLjQsMC41LTAuNiwwLjhjLTEuNywyLjMtMS42LDUuNCwwLjQsNy40ICBjMC4xLDAuMSwwLjIsMC4yLDAuMiwwLjJjMiwyLDUsMi4xLDcuMywwLjVjMCwwLDAsMCwwLjEsMGMxLjctMS4yLDMuMy0yLjgsNS4yLTMuMWM0LjItMC45LDcuNS0zLDEwLjQtNkM0MS4zLDczLjQsNTIuNiw2Miw2NCw1MC43ICBjMC41LTAuNSwxLTAuOSwxLjgtMS43YzAuNSwwLjcsMC44LDEuMywxLjMsMS44YzIuMiwyLjMsNC42LDIuMiw2LjksMGMxLjItMS4yLDIuNC0yLjQsMy42LTMuNmMyLjktMi45LDMuNy00LjMsMS4xLTcuOCAgYzIuNC0yLjQsNC44LTQuNyw3LjItNy4xYzMuMy0zLjQsNy4yLTYuMyw4LjctMTEuMUM5NSwyMCw5NS4xLDE4LjgsOTQuOSwxNy42eiBNNjEuNiw0Ny4yQzQ5LjksNTguOSwzOC4yLDcwLjYsMjYuNSw4Mi4yICBjLTIuMiwyLjItNC43LDMuNi03LjcsNC40Yy0yLjMsMC42LTQuMywyLjItNi40LDMuM2MtMC4yLDAuMS0wLjQsMC4zLTAuNiwwLjRjLTAuNiwwLjUtMS41LDAuNC0yLTAuMWMwLDAsMCwwLDAsMCAgYy0wLjUtMC42LTAuNi0xLjQtMC4xLTJjMC43LTAuOSwxLjQtMS44LDItMi43YzAuOC0xLjMsMS41LTIuOCwxLjgtNC4zYzAuNi0yLjksMS45LTUuMywzLjktNy4zYzEyLjEtMTIuMSwyNC4yLTI0LjIsMzYuMS0zNi4xICBjMi45LDIuOCw1LjcsNS43LDguNyw4LjdDNjIuMiw0Ni41LDYxLjksNDYuOSw2MS42LDQ3LjJ6Ij48L3BhdGg+PC9zdmc+")';
            }

            let pickerStyle = {
                width: '64px',
                height: '64px',
                backgroundColor: color_1_hex,
                backgroundImage: pickerBgUrl,
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center',
                backgroundSize: '48px 48px',
                borderRadius: '32px',
                position: 'absolute',
                marginTop: '-150px',
                right: '-15px',
                cursor: 'pointer'
            };

            var pickerDrawerWidth;

            if (this.state.pickerExpanded === id){
                pickerDrawerWidth = '250px';
            } else {
                pickerDrawerWidth = '64px';
            }

            let pickerDrawerStyle = {
                height: '64px',
                width: pickerDrawerWidth,
                borderRadius: '32px',
                backgroundColor: '#FFFFFF',
                marginTop: '-150px',
                right: '-15px',
                position: 'absolute',
                textAlign: 'left',
                overflow: 'hidden'
            };

            let ColorPicker = () => {
              return (
                  <div>
                      <div style={pickerDrawerStyle}>
                          <div
                              style={colorStyle1}
                              onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64); }} />
                          <div
                              style={colorStyle2}
                              onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_2, siamese_64); }} />
                          <div
                              style={colorStyle3}
                              onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_3, siamese_64); }} />
                      </div>
                      <div style={pickerStyle} onClick={() => { this.expandDrawer(id, this.state.pickerExpanded); }}></div>
                  </div>
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
                    {/*<div className="color-picker"></div>*/}
                    <ColorPicker/>
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
