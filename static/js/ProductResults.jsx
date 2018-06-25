// ProductResults.jsxx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Paper from 'material-ui/Paper';

const categories = {
    'accessories': [
        'backpack',
        'bag',
        'belt',
        'clutch',
        'notebook',
        'pack',
        'scarf',
        'scrunchie',
        'wallet',
        'watch'
    ],
    'head wear': [
        'bandana',
        'beret',
        'glasses',
        'hat',
        'scarf',
        'sunglasses'
    ],
    'theme': [
        'babydoll',
        'glamorous',
        'party',
        'petite',
        'skinny',
        'tall',
        'wedding',
    ],
    'bikini': [
        'top',
        'bottom',
        'floral',
        'lace',
        'plunge',
        'swim',
        'swimsuit'
    ],
    'suit': [
        'blazer',
        'jacket',
        'suit',
        'tie',
        'trousers',
        'waistcoat'
    ],
    'classy': [
        'blouse',
        'jumpsuit',
        'jersey'
    ],
    'dress': [
        'bodycon',
        'cami',
        'corset',
        'dress',
        'embellished',
        'embroider',
        'embroidered',
        'floral',
        'highwaist',
        'jersey',
        'kimono',
        'long',
        'maternity',
        'maxi',
        'midi',
        'mini',
        'pencil',
        'plunge',
        'sequin',
        'skirt',
        'trapeze',
        'tunic'
    ],
    'foot wear': [
        'boots',
        'espadrilles',
        'flats',
        'floral',
        'heels',
        'leather',
        'loafers',
        'mule',
        'office',
        'plimsolls',
        'sandal',
        'shoe',
        'slippers',
        'socks',
        'trainer'
    ],
    'underwear': [
        'body',
        'bottom',
        'bra',
        'brief',
        'embroider',
        'embroidered',
        'knicker',
        'lingerie',
        'maternity',
        'nightwear',
        'pack',
        'pant',
        'plunge',
        'pyjama',
        'thong',
        'trunks'
    ],
    'jewellery': [
        'bracelet',
        'earrings',
        'gold',
        'necklace',
        'pearl',
        'ring'
    ],
    'top': [
        'cami',
        'crop',
        'floral',
        'frill',
        'kimono',
        'maternity',
        'plunge',
        'shirt',
        'tee',
        't-shirt',
        'top',
        'tunic'
    ],
    'knitted': [
        'cardigan',
        'knit',
        'knitted'
    ],
    'trousers': [
        'chino',
        'dungaree',
        'floral',
        'highwaist',
        'jean',
        'jegging',
        'jogger',
        'legging',
        'mom',
        'shorts',
        'tregging',
        'trouser'
    ],
    'outer wear': [
        'coat',
        'parka'
    ],
    'cosmetics': [
        'concealer',
        'contour',
        'eyeliner',
        'highlight',
        'kit',
        'liner',
        'lipstick',
        'mask',
        'mascara',
        'primer'
    ],
    'pattern': [
        'denim',
        'floral',
        'knit',
        'knitted',
        'mesh',
        'polka',
        'print',
        'stripe'
    ],
    'material': [
        'fur',
        'gold',
        'leather',
        'metallic',
        'pearl',
        'satin',
        'velvet'
    ],
    'embellishments': [
        'embellished',
        'embroidered',
        'frill',
        'floral',
        'glitter',
        'gold',
        'lace',
        'mesh',
        'print',
        'ruffle',
        'sequin',
        'quilted',
        'tassel'
    ],
    'casual': [
        'hoodie',
        'jumper',
        'pants',
        'playsuit',
        'pyjama',
        'sweatshirt',
        'tee',
        't-shirt',
        'tracksuit',
        'tregging',
        'vest'
    ],
    'summer': [
        'mini',
        'playsuit',
        'sandal',
        'shorts',
        'tee',
        'vest'
    ],
    'sports': [
        'bra',
        'sweat',
        'tracksuit',
        'trainer'
    ]
};

const higherCats = [
    'accessories',
    'bikini',
    'casual',
    'classy',
    'cosmetics',
    'dress',
    'embellishments',
    'foot wear',
    'head wear',
    'jewellery',
    'knitted',
    'material',
    'outer wear',
    'pattern',
    'suit',
    'sports',
    'summer',
    'theme',
    'top',
    'trousers',
    'underwear'
];

class ProductResults extends React.Component  {
    constructor(props) {
        super(props);
        this.state = {
            pickerExpanded: 0,
            faveDrawerExpanded: 0,
            email: this.props.email,
            faveDrawerWidth: '64px',
            catPickerExpanded: 0
        };
        this.expandDrawer = this.expandDrawer.bind(this);
        this.simImSrc = this.simImSrc.bind(this);
        this.addToFavs = this.addToFavs.bind(this);
        this.setMainCatsAndSearchSimilar = this.setMainCatsAndSearchSimilar.bind(this);
    }

    setMainCatsAndSearchSimilar(mainCat1, mainCat2, nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id){
        console.log('Setting main cat to: ', mainCat1, ' and secondary cat to: ', mainCat2);
        this.setState({
            catPickerExpanded: 0
        });
        this.props.setMainCatsAndSearchSimilar(mainCat1, mainCat2, nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id);
    }

    simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id){
        this.setState({
            pickerExpanded: 0
        });
        console.log('Product results passed id: ', prod_id);
        this.props.simImgSearch(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id);
    }

    // Expands color picker drawer
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

    expandCatDrawer = (id, pickerId) => {
        console.log(id, ' vs ', pickerId);
        if (id === pickerId){
            this.setState({
                catPickerExpanded: 0
            });
        } else {
            this.setState({
                catPickerExpanded: id
            });
        }
    };

    addToFavs = (img_hash, id) => {
        let email = this.state.email;
        // console.log('Add faves email: ', email);
        fetch(window.location.origin + '/api/addfav', {
            method: 'post',
            body: JSON.stringify({email: email, img_hash: img_hash})
        }).then(function(response) { return response.json(); })
            .then(data => {
                console.log(data);

                this.setState({
                    faveDrawerExpanded: id
                });

                setTimeout(() =>{
                    this.setState({
                        faveDrawerExpanded: 0
                    });
                }, 2000);
            });
    };

    render () {
        let tiles = this.props.results.map(product => {
            // console.log('Product data passed to result list: ', product[0]);
            let productInfo = product[0];
            let img_hash = productInfo.img_hash;
            let brand = productInfo.brand;
            let color_1 = productInfo.color_1;
            let color_1_hex = productInfo.color_1_hex;
            let color_2 = productInfo.color_2;
            let color_2_hex = productInfo.color_2_hex;
            let color_3 = productInfo.color_3;
            let color_3_hex = productInfo.color_3_hex;
            let prod_id = productInfo.id;
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

            let catArray = [];
            let catCheckArray = [];

            higherCats.map(hCat => {
                let lCats = categories[hCat];
                let nameArray = name.toLowerCase().split(' ');
                nameArray.map(word => {
                    if (lCats.includes(word)){
                        let pushObj = {
                            'cat': word,
                            'hCat': hCat
                        };
                        if (!catCheckArray.includes(word)){
                            catCheckArray.push(word);
                            catArray.push(pushObj);
                        }
                    }
                });
            });

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

            if (this.state.pickerExpanded === prod_id){
                pickerDrawerWidth = '250px';
            } else {
                pickerDrawerWidth = '64px';
            }

            let pickerDrawerStyle = {
                height: '64px',
                transition: 'width 300ms ease-in-out',
                width: pickerDrawerWidth,
                borderRadius: '32px',
                backgroundColor: '#FFFFFF',
                marginTop: '-150px',
                right: '-15px',
                position: 'absolute',
                textAlign: 'left',
                overflow: 'hidden'
            };

            var faveDrawerWidth;

            if (this.state.faveDrawerExpanded === prod_id){
                faveDrawerWidth = '244px';
            } else {
                faveDrawerWidth = '64px';
            }

            let faveDrawerStyle = {
                height: '64px',
                transition: 'width 300ms ease-in-out',
                width: faveDrawerWidth,
                borderRadius: '32px',
                backgroundColor: '#FFFFFF',
                marginTop: '-310px',
                right: '-15px',
                position: 'absolute',
                textAlign: 'left',
                overflow: 'hidden',
                lineHeight: '64px',
                verticalAlign: 'middle',
                fontSize: '1.5rem',
                paddingLeft: '10px',
                paddingTop: '2px'
            };

            let singleCatStyle = {
                // width: '50px',
                height: '50px',
                borderRadius: '25px',
                backgroundColor: '#f5e8ff',
                margin: '7px',
                marginRight: '0px',
                display: 'inline-block',
                cursor: 'pointer',
                verticalAlign: 'middle',
                textAlign: 'center',
                paddingTop: '13px',
                paddingRight: '5px',
                paddingLeft: '5px'
            };

            var catPickerDrawerWidth;

            if (this.state.catPickerExpanded === prod_id){
                catPickerDrawerWidth = '600px';
            } else {
                catPickerDrawerWidth = '64px';
            }

            let catPickerDrawerStyle = {
                height: '64px',
                transition: 'width 300ms ease-in-out',
                maxWidth: catPickerDrawerWidth,
                borderRadius: '32px',
                backgroundColor: '#FFFFFF',
                marginTop: '-230px',
                right: '-15px',
                position: 'absolute',
                textAlign: 'left',
                overflow: 'hidden',
                paddingRight: '69px'
            };


            let ColorPicker = () => {
                return (
                  <div>
                      <div style={pickerDrawerStyle}>
                          <div
                              style={colorStyle1}
                              onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id); }} />
                          <div
                              style={colorStyle2}
                              onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_2, siamese_64, prod_id); }} />
                          <div
                              style={colorStyle3}
                              onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_3, siamese_64, prod_id); }} />
                      </div>
                      <div style={pickerStyle} onClick={() => { this.expandDrawer(prod_id, this.state.pickerExpanded); }}></div>
                  </div>
                )
            };

            let CatPicker = () => {
                let catItems = catArray.map((catObj, index) => {
                    let mainCat1 = catObj['cat'];
                    // let mainCat2 = catObj['hCat'];
                    let mainCat2 = this.props.mainCat;
                    return (
                        <div
                            key={index}
                            style={singleCatStyle}
                            onClick={() => {
                                this.setMainCatsAndSearchSimilar(mainCat1, mainCat2, nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id); }}>
                            {mainCat1}
                        </div>
                    )
                });
                return (
                    <div>
                        <div style={catPickerDrawerStyle}>
                            {catItems}
                        </div>
                        <div className="cat-picker-bubble" onClick={() => { this.expandCatDrawer(prod_id, this.state.catPickerExpanded); }}></div>
                    </div>
                )
            };

            return (
                <Paper zDepth={1} className="product-tile" key={prod_id}>
                    <div className="product-name">{name}</div>
                    <div className="product-brand"><p>{brand} from {shop}</p></div>
                    <img className="product-image" src={img_url} />
                    <div className={sale ? 'product-price-sale' : 'product-price'}>{sale ? currency+saleprice+', was '+currency+price : currency+price}</div>
                    <div className="search-similar" onClick={() => { this.simImSrc(nr1_cat_ai, nr1_cat_sc, img_cat_sc_txt, color_1, siamese_64, prod_id); }}></div>
                    <ColorPicker/>
                    <CatPicker/>
                    <div style={faveDrawerStyle} >Added to faves</div>
                    <div className="add-to-favorites" onClick={() => { this.addToFavs(img_hash, prod_id); }}></div>
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
