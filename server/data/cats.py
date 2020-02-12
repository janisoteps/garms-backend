class Cats:
    kind_cats = [
        'accessories',
        'activewear',
        'backpack',
        'bag',
        'beachwear',
        'beanie',
        'beauty',
        'belt',
        'bikini',
        'blazer',
        'blouse',
        'bodycon',
        'bodysuit',
        'boot',
        'bottom',
        'bra',
        'bracelet',
        'bralet',
        'bralette',
        'brief',
        'brogues',
        'cami',
        'cape',
        'cardigan',
        'chinos',
        'clutch',
        'coat',
        'corset',
        'culotte',
        'dress',
        'dungaree',
        'earring',
        'earrings',
        'espadrille',
        'gloves',
        'handbag',
        'hat',
        'headband',
        'heel',
        'hoodie',
        'hoody',
        'jacket',
        'jean',
        'jeggings',
        'jersey',
        'jewellery',
        'jogger',
        'jumper',
        'jumpsuit',
        'kimono',
        'knickers',
        'legging',
        'lingerie',
        'lipstick',
        'loafers',
        'makeup',
        'mules',
        'necklace',
        'nightwear',
        'pant',
        'parka',
        'playsuit',
        'polo',
        'pullover',
        'pyjama',
        'ring',
        'rucksack',
        'sandal',
        'scarf',
        'shirt',
        'shoe',
        'shoes',
        'shorts',
        'skirt',
        'sneakers',
        'sock',
        'suit',
        'sundress',
        'sunglasses',
        'sweater',
        'sweatshirt',
        'swim',
        'swimming',
        'swimsuit',
        'swimwear',
        't-shirt',
        't-shirts',
        'tee',
        'thong',
        'tights',
        'top',
        'tote',
        'tracksuit',
        'trainer',
        'trouser',
        'trunks',
        'tunic',
        'tuxedo',
        'underwear',
        'vest',
        'vests',
        'waistcoat',
        'watch',
        'watches',
        'windbreaker',
        'workwear'
    ]
    pattern_cats = [
        'abstract',
        'acid',
        'animal',
        'bright',
        'cable',
        'camo',
        'camouflage',
        'cat',
        'charcoal',
        'check',
        'checked',
        'chevron',
        'circle',
        'clear',
        'contrast',
        'crochet',
        'daisy',
        'dark',
        'diamond',
        'distressed',
        'dot',
        'dye',
        'embellished',
        'embellishment',
        'embroidered',
        'embroidery',
        'floral',
        'flower',
        'geometric',
        'gingham',
        'heart',
        'jacquard',
        'knot',
        'lace',
        'lattice',
        'leopard',
        'light',
        'logo',
        'melange',
        'mesh',
        'metallic',
        'monochrome',
        'paisley',
        'pale',
        'palm',
        'pattern',
        'pinstripe',
        'polka',
        'print',
        'printed',
        'rainbow',
        'rib',
        'snake',
        'spot',
        'square',
        'star',
        'stitch',
        'stripe',
        'striped',
        'stripes',
        'tartan',
        'tea',
        'textured',
        'tiger',
        'tortoiseshell',
        'triangle',
        'tropical',
        'vanilla',
        'wash',
        'washed',
        'zebra'
    ]
    color_cats = [
        'apricot',
        'beige',
        'black',
        'blue',
        'brown',
        'burgundy',
        'camel',
        'cognac',
        'cream',
        'gold',
        'green',
        'grey',
        'heather',
        'honey',
        'indigo',
        'ivory',
        'khaki',
        'lettuce',
        'lilac',
        'lime',
        'mango',
        'matte',
        'mustard',
        'navy',
        'neon',
        'nude',
        'olive',
        'ombre',
        'orange',
        'pale',
        'peach',
        'pink',
        'purple',
        'red',
        'reflective',
        'rose',
        'rust',
        'sand',
        'silver',
        'tan',
        'taupe',
        'white',
        'yellow'
    ]
    style_cats = [
        'a-line',
        'asymmetric',
        'bandeau',
        'bardot',
        'basic',
        'beach',
        'biker',
        'body',
        'bomber',
        'boxy',
        'boyfriend',
        'bridal',
        'broderie',
        'cargo',
        'casual',
        'chelsea',
        'christmas',
        'chunky',
        'classic',
        'club',
        'crop',
        'cropped',
        'cross',
        'curved',
        'derby',
        'ditsy',
        'festival',
        'flare',
        'flared',
        'flat',
        'fluffy',
        'formal',
        'french',
        'fringe',
        'glam',
        'glamorous',
        'gym',
        'high',
        'homme',
        'large',
        'long-sleeve',
        'long',
        'longline',
        'loose',
        'lounge',
        'low',
        'mela',
        'milkmaid',
        'mom',
        'muscle',
        'oversized',
        'oxford',
        'pencil',
        'peplum',
        'petite',
        'pinafore',
        'plain',
        'platform',
        'pleated',
        'plunge',
        'puffer',
        'push-up',
        'quilted',
        'raw',
        'regular',
        'relaxed',
        'retro',
        'ribbed',
        'ripped',
        'ruched',
        'running',
        'sheer',
        'shirred',
        'short',
        'skater',
        'skinny',
        'sleeveless',
        'slim-fit',
        'slim',
        'slinky',
        'slip',
        'smart',
        'smock',
        'south',
        'sport',
        'sporty',
        'stiletto',
        'straight',
        'strappy',
        'summer',
        'tailored',
        'tall',
        'tank',
        'tapered',
        'tie',
        'tiered',
        'track',
        'training',
        'trench',
        'unisex',
        'vintage',
        'wedding',
        'western',
        'wide',
        'winter',
        'wrap'
    ]
    material_cats = [
        'beaded',
        'cashmere',
        'chiffon',
        'chino',
        'cord',
        'corduroy',
        'cotton',
        'crochet',
        'denim',
        'down',
        'faux',
        'fishnet',
        'flannel',
        'fleece',
        'fur',
        'glitter',
        'jacquard',
        'knit',
        'knitted',
        'lace',
        'leather',
        'linen',
        'merino',
        'metal',
        'metallic',
        'nylon',
        'paper',
        'pearl',
        'plisse',
        'poplin',
        'puffer',
        'satin',
        'silk',
        'straw',
        'suede',
        'suedette',
        'tulle',
        'tweed',
        'twill',
        'velour',
        'velvet',
        'viscose',
        'wool',
        'woven'
    ]
    attribute_cats = [
        'ankle',
        'back',
        'backless',
        'belted',
        'block',
        'bow',
        'buckle',
        'bust',
        'button',
        'buttons',
        'cameo',
        'cap',
        'chain',
        'collar',
        'cowl',
        'crewneck',
        'crinkle',
        'cup',
        'diamante',
        'double',
        'drape',
        'embossed',
        'frill',
        'halter',
        'halterneck',
        'heeled',
        'hem',
        'hood',
        'hooded',
        'insert',
        'knee',
        'leg',
        'mid',
        'monogram',
        'neck',
        'open',
        'pack',
        'padded',
        'panel',
        'panelled',
        'pocket',
        'puffer',
        'raglan',
        'ruffle',
        'sequin',
        'sequined',
        'shoulder',
        'skull',
        'sleeve',
        'sleeves',
        'soft',
        'straight-leg',
        'strap',
        'straps',
        'stretch',
        'stud',
        'studded',
        'sweat',
        'tassel',
        'tasselled',
        'trim',
        'turtle',
        'turtleneck',
        'twist',
        'underwire',
        'underwired',
        'up',
        'v-neck',
        'waist',
        'waistband',
        'waisted',
        'zip',
        'zipped'
    ]
    length_cats = [
        'ankle',
        'full',
        'knee',
        'length',
        'long',
        'maxi',
        'mid',
        'mid-rise',
        'midaxi',
        'midi',
        'mini'
    ]
    filter_cats = [
        'curve',
        'curves',
        'mamalicious',
        'maternity',
        'plus'
    ]
    all_cats = kind_cats + pattern_cats + color_cats + style_cats + material_cats + attribute_cats + length_cats + filter_cats
