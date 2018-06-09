import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';


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
    'smart': [
        'blazer',
        'jacket',
        'suit',
        'tie',
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
    'smart',
    'sports',
    'summer',
    'theme',
    'top',
    'trousers',
    'underwear'
];


class CatPicker extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            expandCat: null
        };

        this.expandCatList = this.expandCatList.bind(this);
        this.showCatPicker = this.showCatPicker.bind(this);
        this.setMainCats = this.setMainCats.bind(this);
    }

    expandCatList(key){
        if(key === this.state.expandCat){
            this.setState({
                expandCat: null
            });
        } else {
            this.setState({
                expandCat: key
            })
        }
    }

    showCatPicker(){
        this.props.showCatPicker();
    }

    setMainCats(mainCat, mainCat2){
        this.props.setMainCats(mainCat, mainCat2);
    }
    // Main render
    render () {

        let catList = higherCats.map((hCat, ind) => {
            // console.log('Hcat: ', hCat, ' index: ', ind);
            // console.log('categories: ', categories);
            let cats = categories[hCat].map((cat, ind) => {
                let catStyle = {
                    borderWidth: this.props.mainCat === cat && '1px',
                    borderColor: this.props.mainCat === cat && '#ab99b8',
                    borderStyle: this.props.mainCat === cat && 'solid'
                };
                return(
                    <div style={catStyle}>
                        <div
                        key={'cat-line' + ind}
                        className="cat-line"
                        onClick={() => {this.setMainCats(cat, hCat);}}
                        >{cat}</div>
                    </div>
                )
            });

            return(
                <div className="cat-picker-expand" key={ind} onClick={() => {this.expandCatList(ind);}}>
                    <div className="picker-title"><i className="cat-icon" /> {hCat}</div>
                    {(this.state.expandCat === ind) && (
                        cats
                    )}
                </div>
            )
        });

        return (
            <MuiThemeProvider>
                <div className="cat-picker-modal">
                    <div className="close-cat-picker" onClick={this.showCatPicker}></div>
                    <div className="cat-picker-title"><p>I'm thinking of... {this.props.mainCat2} {this.props.mainCat}</p></div>
                    {catList}
                </div>
            </MuiThemeProvider>
        )
    }
}

export default CatPicker;
