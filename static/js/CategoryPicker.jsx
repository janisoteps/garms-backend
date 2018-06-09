// CategoryPicker.jsx
import React from "react";
require('../css/garms.css');
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Paper from 'material-ui/Paper';
import ImageSearch from "./ImageSearch";

const categories = [
    'Babydoll',
    'Backpack',
    'Bag',
    'Bandana',
    'Belt',
    'Beret',
    'Bikini',
    'Blazer',
    'Blouse',
    'Body',
    'Bodycon',
    'Boots',
    'Bottom',
    'Bra',
    'Bracelet',
    'Brief',
    'Cami',
    'Cardigan',
    'Chino',
    'Clutch',
    'Coat',
    'Concealer',
    'Contour',
    'Corset',
    'Crop',
    'Denim',
    'Dress',
    'Dungaree',
    'Earrings',
    'Embellished',
    'Embroider',
    'Espadrilles',
    'Eyeliner',
    'Flask',
    'Flats',
    'Floral',
    'Frill',
    'Fur',
    'Glamorous',
    'Glasses',
    'Glitter',
    'Gold',
    'Hat',
    'Heels',
    'Highwaist',
    'Highlight',
    'Hoodie',
    'Jacket',
    'Jean',
    'Jegging',
    'Jersey',
    'Jogger',
    'Jumper',
    'Jumpsuit',
    'Kimono',
    'Kit',
    'Knickers',
    'Knit',
    'Knitted',
    'Lace',
    'Leather',
    'Legging',
    'Lingerie',
    'Liner',
    'Lipstick',
    'Loafers',
    'Long',
    'Mask',
    'Maternity',
    'Mascara',
    'Maxi',
    'Mesh',
    'Metallic',
    'Midi',
    'Mini',
    'Mom',
    'Mule',
    'Necklace',
    'Nightwear',
    'Notebook',
    'Office',
    'Pack',
    'Pant',
    'Park',
    'Parka',
    'Pearl',
    'Pencil',
    'Petite',
    'Playsuit',
    'Plimsolls',
    'Plunge',
    'Polka',
    'Primer',
    'Print',
    'Pyjama',
    'Quilted',
    'Ring',
    'Ruffle',
    'Sandal',
    'Satin',
    'Scarf',
    'Scrunchie',
    'Sequin',
    'Shirt',
    'Shoe',
    'Short',
    'Shorts',
    'Skinny',
    'Skirt',
    'Slippers',
    'Socks',
    'Stripe',
    'Suit',
    'Sunglasses',
    'Sweat',
    'Sweatshirt',
    'Swim',
    'Swimsuit',
    'Tee',
    'T-Shirt',
    'Tall',
    'Tassel',
    'Thong',
    'Tie',
    'Top',
    'Tracksuit',
    'Trainer',
    'Trapeze',
    'Tregging',
    'Trouser',
    'Trunks',
    'Tunic',
    'Velvet',
    'Vest',
    'Waistcoat',
    'Wallet',
    'Watch',
    'Wedding'
];

class CategoryPicker extends React.Component  {
    constructor(props) {
        super(props);
    }

    // Main render
    render () {

        categories.forEach(category => {
            let catInd = categories.indexOf(category);
            return(
                <div className="cat-picker-line" key={catInd}>category</div>
            )
        });

        return (
            <div>
                <MuiThemeProvider>

                </MuiThemeProvider>
            </div>
        )
    }
}

export default CategoryPicker;
