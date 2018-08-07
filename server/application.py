from random import shuffle
import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
import scipy.spatial as spatial
import numpy as np
from marshmallow import Schema, fields
from operator import itemgetter
import string
from sqlalchemy import func, any_, or_
from color_text import color_check
import asyncio
import aiohttp


application = app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Product, Products, Images


# # # # # # # Marshmallow schemas


class ProductSchema(Schema):
    id = fields.Integer()
    img_hash = fields.String()
    prod_url = fields.String()
    name = fields.String()
    description = fields.String()
    brand = fields.String()
    shop = fields.String()
    date = fields.Number()
    sex = fields.String()
    currency = fields.String()
    price = fields.Number()
    sale = fields.Boolean()
    saleprice = fields.Number()
    img_url = fields.String()  # Scraped image source
    img_urls = fields.List(fields.String())  # Rest of product scraped images
    spider_cat = fields.String()
    img_cats_ai_txt = fields.List(fields.String())  # Image categories assigned by AI analysis text format
    img_cats_sc_txt = fields.List(fields.String())  # Image categories from scraped name in text format
    color_name = fields.String()  # Text color value from scraped resources
    color_512 = fields.List(fields.Integer())  # Array of 512 integers representing 3D color vector
    color_1 = fields.List(fields.Integer())  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = fields.String()
    color_2 = fields.List(fields.Integer())
    color_2_hex = fields.String()
    color_3 = fields.List(fields.Integer())
    color_3_hex = fields.String()
    pca_256 = fields.List(fields.Integer())
    siamese_64 = fields.List(fields.Integer())
    pattern_256 = fields.List(fields.Integer())


class ProductsSchema(Schema):
    id = fields.Integer()
    prod_hash = fields.String()
    prod_url = fields.String()
    name = fields.String()
    description = fields.String()
    brand = fields.String()
    shop = fields.String()
    date = fields.Number()
    sex = fields.String()
    currency = fields.String()
    price = fields.Number()
    sale = fields.Boolean()
    saleprice = fields.Number()
    img_url = fields.String()  # Scraped image source
    img_urls = fields.List(fields.String())  # Rest of product scraped images
    img_hashes = fields.List(fields.String())
    spider_cat = fields.String()
    img_cats_sc_txt = fields.List(fields.String())  # Image categories from scraped name in text format


class ImageSchema(Schema):
    id = fields.Integer()
    img_hash = fields.String()
    prod_url = fields.String()
    img_url = fields.String()  # Scraped image source
    name = fields.String()
    description = fields.String()
    brand = fields.String()
    shop = fields.String()
    date = fields.Number()
    sex = fields.String()
    currency = fields.String()
    price = fields.Number()
    sale = fields.Boolean()
    saleprice = fields.Number()
    spider_cat = fields.String()
    img_cats_ai_txt = fields.List(fields.String())  # Image categories assigned by AI analysis text format
    img_cats_sc_txt = fields.List(fields.String())  # Image categories from scraped name in text format
    color_name = fields.String()  # Text color value from scraped resources
    color_512 = fields.List(fields.Float())  # Array of 512 floats representing 3D color vector
    color_1 = fields.List(fields.Integer())  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = fields.String()
    color_2 = fields.List(fields.Integer())
    color_2_hex = fields.String()
    color_3 = fields.List(fields.Integer())
    color_3_hex = fields.String()
    encoding_nocrop = fields.List(fields.Integer())
    encoding_crop = fields.List(fields.Integer())
    encoding_squarecrop = fields.List(fields.Integer())


# # # # # # # Functions # # # # # # #


def create_user():
    return 'user :)'
    # with db.connect() as conn:


# Make console output pretty
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Function to get rid of any invisible chars
def filter_out_junk(text):
    return ''.join(x for x in text if x in set(string.printable))


def hex_to_rgb(value):
    value = filter_out_junk(value)
    value = value[2:]
    lv = len(value)
    # print('length: ', str(lv))
    # print('Value: ', str(value))
    return tuple(int(value[i:i + int(lv / 3)], 16) for i in range(0, lv, int(lv / 3)))


async def call_url(url, image):
    print('Starting {}'.format(url))
    response = await aiohttp.get(url)
    data = await response.text()
    print('{}: {} bytes: {}'.format(url, len(data), data))
    return data


async def send_file(url, image_file):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            'image': image_file
        }) as response:
            data = await response.text()
            print(data)
            return data


# # # # # # # API functions # # # # # # #


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        email = data['email']
        pwd = data['pwd']
        sex = data['sex']
        username = data['username']
        fb_id = str(np.random.random() * 1000)

        user = User.query.filter_by(email=email).first()

        # If no such email exists in DB create a new user submission
        if user is None:
            reg_submission = User(
                username=username,
                email=email,
                sex=sex,
                password=pwd,
                fb_id=fb_id,
                favorites_ids=''
            )
            db.session.add(reg_submission)
            db.session.commit()

            return json.dumps(True)

        else:
            return json.dumps(False)


@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        print('Data: ', str(request.data))
        email = data['email']
        pwd = data['pwd']
        user = User.query.filter_by(email=email).first()

        # print('User: ', str(user))
        if user is None or not user.check_password(pwd):
            return json.dumps(False)

        else:
            user_id = user.id
            username = user.username
            favorites = user.favorites_ids
            sex = user.sex
            user_email = user.email

            # print(username)
            user_dict = {
                'user_id': user_id,
                'username': username,
                'favorites': favorites,
                'sex': sex,
                'email': user_email
            }

            res = jsonify(auth=True, res=user_dict)

            return res


@app.route("/api/addfav", methods=['POST'])
def addfav():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        print('Data: ', str(data))
        img_hash = data['img_hash']
        if len(img_hash) == 40:
            user_email = data['email']

            user = User.query.filter_by(email=user_email).first()

            user.favorites_ids = list(user.favorites_ids)
            user.favorites_ids.append(img_hash)

            db.session.commit()

            return json.dumps(True)


@app.route("/api/removefav", methods=['POST'])
def removefav():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        img_hash = data['img_hash']
        print('len img_hash: ', str(len(img_hash)))
        if len(img_hash) == 40:
            user_email = data['email']

            print('user email: ', str(user_email))
            user = User.query.filter_by(email=user_email).first()

            user.favorites_ids = list(user.favorites_ids)

            if img_hash in user.favorites_ids:
                user.favorites_ids.remove(img_hash)

                db.session.commit()

            # Declare Marshmallow schema so that SqlAlchemy object can be serialized
            product_schema = ProductSchema()

            result_list = []
            for img_hash in user.favorites_ids:
                prod_search = db.session.query(Product).filter((Product.img_hash == img_hash)).first()
                prod_serial = product_schema.dump(prod_search)
                result_list.append(prod_serial)

            res = jsonify(res=result_list)

            print('res: ', str(res))

            return res


@app.route("/api/favorites", methods=['GET'])
def favorites():
    if request.method == 'GET':
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first()
        favs = user.favorites_ids
        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        result_list = []
        for img_hash in favs:
            print('Search img hash: ', str(img_hash))
            prod_search = db.session.query(Product).filter((Product.img_hash == img_hash)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        res = jsonify(res=result_list)

        return res


@app.route('/api/logout')
def logout():
    return json.dumps('OK')


# Upload new product image to database
@app.route("/api/commit_image", methods=['post'])
def commit():
    if request.method == 'POST':
        data = request.get_json(force=True)

        print(str(data))

        img_hash = data['img_hash']
        prod_url = data['prod_url']
        img_url = data['img_url']
        name = data['name']
        description = data['description']
        brand = data['brand']
        shop = data['shop']
        date = data['date']
        sex = data['sex']
        currency = data['currency']
        price = data['price']
        sale = data['sale']
        saleprice = data['saleprice']
        spider_cat = data['spider_cat']
        img_cats_ai_txt = data['img_cats_ai_txt']
        img_cats_sc_txt = data['img_cats_sc_txt']
        color_name = data['color_name']
        color_512 = data['color_512']
        color_1 = data['color_1']
        color_1_hex = data['color_1_hex']
        color_2 = data['color_2']
        color_2_hex = data['color_2_hex']
        color_3 = data['color_3']
        color_3_hex = data['color_3_hex']
        encoding_nocrop = data['encoding_nocrop']
        encoding_crop = data['encoding_crop']
        encoding_squarecrop = data['encoding_squarecrop']

        product_submission = Images(
            img_hash=img_hash,
            prod_url=prod_url,
            img_url=img_url,
            name=name,
            description=description,
            brand=brand,
            shop=shop,
            date=date,
            sex=sex,
            currency=currency,
            price=price,
            sale=sale,
            saleprice=saleprice,
            spider_cat=spider_cat,
            img_cats_ai_txt=img_cats_ai_txt,
            img_cats_sc_txt=img_cats_sc_txt,
            color_name=color_name,
            color_512=color_512,
            color_1=color_1,
            color_1_hex=color_1_hex,
            color_2=color_2,
            color_2_hex=color_2_hex,
            color_3=color_3,
            color_3_hex=color_3_hex,
            encoding_nocrop=encoding_nocrop,
            encoding_crop=encoding_crop,
            encoding_squarecrop=encoding_squarecrop
        )

        try:
            existing_image = Images.query.filter_by(img_hash=img_hash).first()
        except:
            existing_image = None

        if existing_image is None:
            print('Adding a new product')
            db.session.add(product_submission)
            db.session.commit()
            return json.dumps(True)

        else:
            print('Updating existing product')

            existing_image.prod_url = prod_url
            existing_image.name = name
            existing_image.description = description
            existing_image.brand = brand
            existing_image.shop = shop
            existing_image.date = date
            existing_image.sex = sex
            existing_image.currency = currency
            existing_image.price = price
            existing_image.sale = sale
            existing_image.saleprice = saleprice
            existing_image.img_url = img_url
            existing_image.img_urls = img_urls
            existing_image.spider_cat = spider_cat
            existing_image.img_cats_ai_txt = img_cats_ai_txt
            existing_image.img_cats_sc_txt = img_cats_sc_txt
            existing_image.color_name = color_name
            existing_image.color_512 = color_512
            existing_image.color_1 = color_1
            existing_image.color_1_hex = color_1_hex
            existing_image.color_2 = color_2
            existing_image.color_2_hex = color_2_hex
            existing_image.color_3 = color_3
            existing_image.color_3_hex = color_3_hex
            existing_image.encoding_nocrop = encoding_nocrop
            existing_image.encoding_crop = encoding_crop
            existing_image.encoding_squarecrop = encoding_squarecrop

            db.session.commit()
            return json.dumps(True)


# Upload new product object to database
@app.route("/api/commit_product", methods=['post'])
def commit():
    if request.method == 'POST':
        data = request.get_json(force=True)

        print(str(data))

        prod_hash = data['prod_hash']
        prod_url = data['prod_url']
        name = data['name']
        description = data['description']
        brand = data['brand']
        shop = data['shop']
        date = data['date']
        sex = data['sex']
        currency = data['currency']
        price = data['price']
        sale = data['sale']
        saleprice = data['saleprice']
        img_url = data['img_url']
        img_urls = data['img_urls']
        img_hashes = data['img_hashes']
        spider_cat = data['spider_cat']
        img_cats_sc_txt = data['img_cats_sc_txt']

        product_submission = Products(
            prod_hash=prod_hash,
            prod_url=prod_url,
            name=name,
            description=description,
            brand=brand,
            shop=shop,
            date=date,
            sex=sex,
            currency=currency,
            price=price,
            sale=sale,
            saleprice=saleprice,
            img_url=img_url,
            img_urls=img_urls,
            img_hashes=img_hashes,
            spider_cat=spider_cat,
            img_cats_sc_txt=img_cats_sc_txt
        )

        try:
            existing_product = Products.query.filter_by(prod_hash=prod_hash).first()
        except:
            existing_product = None

        if existing_product is None:
            print('Adding a new product')
            db.session.add(product_submission)
            db.session.commit()
            return json.dumps(True)

        else:
            print('Updating existing product')

            existing_product.prod_hash = prod_hash
            existing_product.prod_url = prod_url
            existing_product.name = name
            existing_product.description = description
            existing_product.brand = brand
            existing_product.shop = shop
            existing_product.date = date
            existing_product.sex = sex
            existing_product.currency = currency
            existing_product.price = price
            existing_product.sale = sale
            existing_product.saleprice = saleprice
            existing_product.img_url = img_url
            existing_product.img_urls = img_urls
            existing_product.img_hashes = img_hashes
            existing_product.spider_cat = spider_cat
            existing_product.img_cats_sc_txt = img_cats_sc_txt

            db.session.commit()
            return json.dumps(True)


# Search for similar products based on selected product
@app.route("/api/delete", methods=['get'])
def delete():
    if request.method == 'GET':
        img_hash = request.args.get('img_hash')
        shop = request.args.get('shop')

        if len(img_hash) > 0:
            try:
                existing_product = Product.query.filter_by(img_hash=img_hash).first()
            except:
                existing_product = None
            if existing_product is not None:
                db.session.delete(existing_product)
                db.session.commit()
                return json.dumps(True)
            else:
                return json.dumps(False)

        if len(shop) > 0:
            try:
                shop_products = db.session.query(Product).filter(Product.shop == 'Zalando').order_by(
                    func.random()).all()
                db.session.delete(shop_products)
                db.session.commit()
                return json.dumps(True)
            except:
                return json.dumps(False)


# Search for similar products based on selected product
@app.route("/api/search", methods=['get'])
def search():
    if request.method == 'GET':
        main_cat = request.args.get('main_cat')
        main_cat2 = request.args.get('main_cat2')
        req_color_1 = request.args.get('color_1').strip('\'[]').split(',')

        sex = request.args.get('sex')
        request_prod_id = int(request.args.get('id'))
        req_product = Product.query.filter_by(id=request_prod_id).first()
        print('Request ID: ', str(request_prod_id))

        if req_color_1 is None:
            return json.dumps('BAD REQUEST')

        print('Main cat: ', str(main_cat))
        print('Main cat without s: ', str(main_cat[:-1]))

        # Start off by doing the initial query looking for categories
        id_list = db.session.query(Product).filter(
            ((Product.img_cats_ai_txt.any(main_cat)) | (Product.spider_cat == main_cat) | (
                Product.img_cats_sc_txt.any(main_cat))) & (Product.sex == sex) & (Product.shop != 'Zalando')).order_by(
            func.random()).limit(5000).all()

        if len(id_list) < 1000:
            id_list = id_list + db.session.query(Product).filter(
                ((Product.img_cats_ai_txt.any(main_cat[:-1])) | (Product.spider_cat == main_cat[:-1]) |
                 (Product.img_cats_sc_txt.any(main_cat[:-1]))) & (Product.sex == sex) & (Product.shop != 'Zalando')) \
                .order_by(func.random()).limit(5000).all()

        print('Amount of returned prods from db: ', str(len(id_list)))

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        # Build a list of ids and color distances from query product
        color_dist_list = []
        for prod_obj in id_list:

            color_prod_id = prod_obj.id
            # print('Color check product ID: ', str(color_prod_id))
            color1_rgb = prod_obj.color_1
            color2_rgb = prod_obj.color_2
            # color3_rgb = prod_obj.color_3

            try:
                image_prod_name = prod_obj.name
            except:
                image_prod_name = None

            if image_prod_name is not None:
                image_prod_name = image_prod_name.strip('\'[]')
                image_prod_name_arr = image_prod_name.lower().split(' ')

                if main_cat in image_prod_name_arr or main_cat[:-1] in image_prod_name_arr:
                    # Use euclidean distance to measure how similar the color is in RGB space
                    # And then to measure how close the siamese encoding is 64 dimensional space
                    distance_color = int(
                        spatial.distance.euclidean(np.array(req_color_1, dtype=int), np.array(color1_rgb, dtype=int),
                                                   w=None))

                    distance_color_2 = int(
                        spatial.distance.euclidean(np.array(req_color_1, dtype=int), np.array(color2_rgb, dtype=int),
                                                   w=None))

                    rgb_req = np.array(req_color_1, dtype=int)
                    rgb_test = np.array(color1_rgb, dtype=int)
                    rgb_req_norm = rgb_req - np.amin(rgb_req)
                    rgb_test_norm = rgb_test - np.amin(rgb_test)
                    # print('Norm Req Color RGB: ', str(rgb_req_norm))
                    # print('Norm Test Color RGB: ', str(rgb_test_norm))
                    distance_color_norm = int(spatial.distance.euclidean(rgb_req_norm, rgb_test_norm, w=None))
                    distance_color = distance_color + distance_color_norm + distance_color_2

                    main_cat2_dist = 1
                    if main_cat2 in image_prod_name_arr:
                        main_cat2_dist = 0

                    main_color_dist = distance_color

                    item_obj = {
                        'id': color_prod_id,
                        'color_distance': main_color_dist,
                        'prod_obj': prod_obj,
                        'main_cat2_dist': main_cat2_dist
                    }

                    color_dist_list.append(item_obj)

        # Try to keep only those items that match both categories
        maincat_list = [d for d in color_dist_list if d['main_cat2_dist'] == 0]

        # Revert to to single main category match if that removes too many results
        if len(maincat_list) < 10:
            maincat_list = color_dist_list

        # Closest colors at top
        sorted_color_list = sorted(maincat_list, key=itemgetter('color_distance'))
        top_color_list = sorted_color_list[0:60]

        # # Calculate PCA encoding distances
        # pca_dist_list = []
        # for color_obj in top_color_list:
        #     req_pca = req_product.pca_256
        #     test_pca = color_obj['prod_obj'].pca_256
        #     if test_pca is not None:
        #         color_distance = color_obj['color_distance']
        #         distance_pca = int(
        #             spatial.distance.euclidean(np.array(req_pca, dtype=int), np.array(test_pca, dtype=int),
        #                                        w=None))
        #         print('PCA distance: ', str(distance_pca))
        #         item_obj = {
        #             'id': color_obj['id'],
        #             'distance_pca': distance_pca,
        #             'color_distance': color_distance,
        #             'prod_obj': color_obj['prod_obj']
        #         }
        #         pca_dist_list.append(item_obj)
        #
        # # Closest PCA at top
        # sorted_pca_list = sorted(pca_dist_list, key=itemgetter('distance_pca'))
        # top_pca_list = sorted_pca_list[0:60]

        # # Calculate siamese encoding distances
        # siamese_dist_list = []
        # for pca_obj in top_pca_list:
        #     test_siamese_64 = pca_obj['prod_obj'].siamese_64
        #     color_distance = pca_obj['color_distance']
        #     distance_siam = int(
        #         spatial.distance.euclidean(np.array(siamese_64, dtype=int), np.array(test_siamese_64, dtype=int),
        #                                    w=None))
        #
        #     # distance = color_obj['color_distance'] + distance_siam
        #     item_obj = {
        #         'id': pca_obj['id'],
        #         'siam_distance': distance_siam,
        #         'color_distance': color_distance,
        #         'distance_pca': pca_obj['distance_pca']
        #     }
        #     siamese_dist_list.append(item_obj)

        # # Make sure we return the original request image back on top
        # if not any(d['id'] == request_prod_id for d in siamese_dist_list):
        #     siamese_dist_list.insert(0, {'id': request_prod_id, 'siam_distance': -1000, 'color_distance': -1000})
        #     print('Product not in list, need to add')
        # else:
        #     print('Product already in list, need to make sure its on top')
        #     request_prod = next(item for item in siamese_dist_list if item['id'] == request_prod_id)
        #     request_prod['siam_distance'] = -1000
        #     request_prod['color_distance'] = -1000
        #
        # # Closest siamese at top
        # sorted_siam_list = sorted(siamese_dist_list, key=itemgetter('siam_distance'))
        # top_siam_list = sorted_siam_list[0:70]
        #
        # # Resort again for color, just for looks :)
        # sorted_list = sorted(top_siam_list, key=itemgetter('color_distance'))

        # Make sure we return the original request image back on top
        if not any(d['id'] == request_prod_id for d in top_color_list):
            top_color_list.insert(0, {'id': request_prod_id, 'siam_distance': -1000, 'color_distance': -1000})
            print('Product not in list, need to add')
        else:
            print('Product already in list, need to make sure its on top')
            request_prod = next(item for item in top_color_list if item['id'] == request_prod_id)
            request_prod['siam_distance'] = -1000
            request_prod['color_distance'] = -1000

        # Resort again for color, just for looks :)
        # sorted_list = sorted(top_pca_list, key=itemgetter('color_distance'))

        # Only top results are returned
        # top_list = sorted_list[0:60]

        result_list = []
        for obj in top_color_list:
            result_obj_id = obj['id']
            prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        # Make it HTTP friendly
        res = jsonify(res=result_list)
        # print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


# Search for products with a search string
@app.route("/api/text", methods=['get'])
def text():
    if request.method == 'GET':
        search_string = request.args.get('string')
        sex = request.args.get('sex')

        print('Text search with string: ', str(search_string))
        # cleaned_string = search_string.translate(' ', "!@£$%^&*()<>?/|~`.,:;#+=_")

        string_list = search_string.strip().lower().split()
        print('string list', str(string_list))
        linking_words = ['with', 'on', 'under', 'over', 'at', 'like', 'in', 'for', 'as', 'after']

        string_list_clean = [e for e in string_list if e not in linking_words]

        color_word_dict = color_check(string_list_clean)

        print(color_word_dict)
        word_list = color_word_dict['words']
        color_list = color_word_dict['colors']

        id_list = []
        if 2 > len(word_list) > 0 and len(color_list) > 0:
            print('1 word and is color')
            id_list += db.session.query(Product).filter(
                (Product.sex == sex) & (func.lower(Product.name).contains(word_list[-1])) & (
                    func.lower(Product.color_name).contains(color_list[0]))).order_by(func.random()).limit(60).all()

        elif 3 > len(word_list) > 1 and len(color_list) > 0:
            print('2 words and is color')
            id_list += db.session.query(Product).filter(
                (Product.sex == sex) & (func.lower(Product.name).contains(word_list[-1])) & (
                    func.lower(Product.name).contains(word_list[1])) & (
                    func.lower(Product.color_name).contains(
                        color_list[0]))).order_by(func.random()).limit(60).all()

        elif 3 > len(word_list) > 1:
            print('2 words, no color')
            id_list += db.session.query(Product).filter(
                (Product.sex == sex) & (func.lower(Product.name).contains(word_list[0])) & (
                    func.lower(Product.name).contains(word_list[1]))).order_by(func.random()).limit(60).all()

        elif 4 > len(word_list) > 2:
            print('3 words, no color')
            id_list += db.session.query(Product).filter(
                (Product.sex == sex) & (func.lower(Product.name).contains(word_list[0])) & (
                    func.lower(Product.name).contains(word_list[1])) & (
                    func.lower(Product.name).contains(word_list[2]))).order_by(
                func.random()).limit(60).all()
            # word_len = len(word_list)
            # for i in range(0, word_len):
            #     id_list += db.session.query(Product).filter(
            #         (func.lower(Product.name).contains(word_list[i]))).order_by(
            #         func.random()).limit(30).all()
        elif 2 > len(word_list) > 0:
            print('1 word, no color')
            id_list += db.session.query(Product).filter(
                (Product.sex == sex) & (func.lower(Product.name).contains(word_list[-1]))).order_by(
                func.random()).limit(60).all()

        elif len(color_list) > 0:
            print('only color')
            color_len = len(color_list)
            for k in range(0, color_len):
                id_list += db.session.query(Product).filter(
                    (Product.sex == sex) & (func.lower(Product.color_name).contains(color_list[k]))).order_by(
                    func.random()).limit(60).all()

        else:
            return json.dumps('BAD REQUEST')

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        result_list = []
        for prod_id in id_list:
            # prod_id_str = str(prod_id)
            # text_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]
            text_prod_id = prod_id.id
            prod_search = db.session.query(Product).filter((Product.id == text_prod_id)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        main_cat = ''
        if len(word_list) > 0:
            main_cat = word_list[-1]

        # Make it HTTP friendly
        res = jsonify(res=result_list, mainCat=main_cat)
        print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


@app.route("/api/color", methods=['POST'])
def query_color():
    if request.method == 'POST':
        if request.files.get("image"):
            print('Got color search request')
            post_image = request.files["image"].read()
            color_api = 'http://34.242.36.122/api/color'

            task = send_file(color_api, post_image)

            loop = asyncio.get_event_loop()

            # Gather response from API using asyncio
            color_response = loop.run_until_complete(task)

            color_1 = json.loads(color_response)['res']['color_1']
            color_1_hex = json.loads(color_response)['res']['color_1_hex']

            color_2 = json.loads(color_response)['res']['color_2']
            color_2_hex = json.loads(color_response)['res']['color_2_hex']

            color_3 = json.loads(color_response)['res']['color_3']
            color_3_hex = json.loads(color_response)['res']['color_3_hex']

            results = {
                'color_1': color_1,
                'color_1_hex': color_1_hex,
                'color_2': color_2,
                'color_2_hex': color_2_hex,
                'color_3': color_3,
                'color_3_hex': color_3_hex
            }

            # Make it HTTP friendly
            res = jsonify(res=results)

            return res


# Return color and category predictions from uploaded image
@app.route("/api/colorcat", methods=['POST'])
def colorcat():
    if request.method == 'POST':
        if request.files.get("image"):
            post_image = request.files["image"].read()
            # post_image = BytesIO(request.files["image"].read())
            print('Got color and category predict request')

            # Two AI APIs have been successfully built
            color_api = 'http://34.242.36.122/api/color'
            # cat_api = 'http://34.243.167.38/api/cats'
            cat_api = 'http://52.18.195.227/api/cats'
            # pca_api = 'http://34.247.218.207:5000/api/encoding'

            api_urls = [color_api, cat_api]

            tasks = [send_file(url, post_image) for url in api_urls]
            loop = asyncio.get_event_loop()
            # Gather responses from APIs using asyncio
            color_response, cat_response = loop.run_until_complete(asyncio.gather(*tasks))

            # if np.isnan(float(json.loads(pca_response)['res']['pca_256'][0])):
            #     pca_retry_task = send_file(pca_api, post_image)
            #     pca_retry_response = loop.run_until_complete(pca_retry_task)
            #     pca_response = pca_retry_response

            img_cats_ai_txt = json.loads(cat_response)['res']['img_cats_ai_txt']
            alt_cats_txt = json.loads(cat_response)['res']['alt_cats_txt']

            for img_cat_ai in img_cats_ai_txt:
                if img_cat_ai in alt_cats_txt:
                    alt_cats_txt.remove(img_cat_ai)

            color_1 = json.loads(color_response)['res']['color_1']
            color_1_hex = json.loads(color_response)['res']['color_1_hex']
            color_2 = json.loads(color_response)['res']['color_2']
            color_2_hex = json.loads(color_response)['res']['color_2_hex']
            color_3 = json.loads(color_response)['res']['color_3']
            color_3_hex = json.loads(color_response)['res']['color_3_hex']
            # pca_256 = json.loads(pca_response)['res']['pca_256']

            results = {
                'img_cats_ai_txt': img_cats_ai_txt,
                'alt_cats_txt': alt_cats_txt,
                'colors': {
                    'color_1': color_1,
                    'color_1_hex': color_1_hex,
                    'color_2': color_2,
                    'color_2_hex': color_2_hex,
                    'color_3': color_3,
                    'color_3_hex': color_3_hex
                }
            }

            # Make it HTTP friendly
            res = jsonify(res=results)

            return res


# Search for products based on chosen color and category
@app.route("/api/colorcatsearch", methods=['get'])
def colorcatsearch():
    if request.method == 'GET':
        cat_ai_txt = request.args.get('cat_ai_txt')
        color_rgb = request.args.get('color_rgb').strip('\'[]').split(',')
        # pca_256 = request.args.get('pca_256').strip('\'[]').split(',')
        # pca_256 = [int(float(i)) for i in pca_256]
        sex = request.args.get('sex')

        # print('Request PCA: ', str(pca_256))
        id_list = db.session.query(Product).filter(
            Product.img_cats_sc_txt.any(cat_ai_txt) & (Product.sex == sex) & (Product.shop != 'Zalando')).order_by(
            func.random()).limit(5000).all()

        color_dist_list = []
        for prod_id in id_list:
            image_prod_id = prod_id.id

            color1_rgb = prod_id.color_1
            color2_rgb = prod_id.color_2
            try:
                image_prod_name = prod_id.name
            except:
                image_prod_name = None

            if image_prod_name is not None:
                image_prod_name = image_prod_name.strip('\'[]')
                image_prod_name_arr = image_prod_name.lower().split(' ')

                print('name array: ', str(image_prod_name_arr))

                distance_color_1 = int(
                    spatial.distance.euclidean(np.array(color_rgb, dtype=int), np.array(color1_rgb, dtype=int),
                                               w=None))

                distance_color_2 = int(
                    spatial.distance.euclidean(np.array(color_rgb, dtype=int), np.array(color2_rgb, dtype=int),
                                               w=None))

                distance_color = (distance_color_1 + distance_color_2) / 2

                if cat_ai_txt in image_prod_name_arr:
                    print(BColors.OKBLUE + 'Color distance: ' + BColors.ENDC + str(distance_color))

                    item_obj = {'id': image_prod_id, 'distance': distance_color, 'prod_string': prod_id}

                    color_dist_list.append(item_obj)

        # Closest colors at top
        color_sorted_list = sorted(color_dist_list, key=itemgetter('distance'))
        top_color_list = color_sorted_list[0:60]

        # Find most similar as per close cropped siamese encoding euclidean distance
        # pca_dist_list = []
        # for prod_obj in top_color_list:
        #     test_pca_256 = prod_obj['prod_string'].pca_256
        #     print('Test PCA: ', str(test_pca_256))
        #
        #     distance_pca = int(
        #         spatial.distance.euclidean(np.array(pca_256, dtype=int), np.array(test_pca_256, dtype=int),
        #                                    w=None))
        #
        #     print(BColors.OKGREEN + 'Siamese distance: ' + BColors.ENDC + str(distance_pca))
        #
        #     # distance = prod_obj['color_distance'] + distance_pca
        #     distance = distance_pca
        #
        #     item_obj = {'id': prod_obj['id'], 'distance': distance}
        #
        #     pca_dist_list.append(item_obj)
        #
        # # Only top results are returned
        # top_list = pca_dist_list[0:60]

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        # Now return db fields of these top similar prods to client
        result_list = []
        for obj in top_color_list:
            result_obj_id = obj['id']
            prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        # Make it HTTP friendly
        res = jsonify(res=result_list)

        # res = jsonify(res=response)
        print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


@app.route("/api/prod_stats", methods=['GET'])
def prods_tats():
    if request.method == 'GET':

        request_type = request.args.get('req_type')

        if request_type == "brand_count":
            products_list = db.session.query(Product).filter().all()

            product_brands = {}
            prod_brand_set = set()
            for product in products_list:
                if product.brand in prod_brand_set:
                    product_brands[product.brand] += 1
                else:
                    prod_brand_set.add(product.brand)
                    product_brands[product.brand] = 1

            res = jsonify(product_brands)

            return res


@app.route("/api/explorer_search", methods=['POST'])
def explorer_search():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        main_cat_top = data['main_cat_top']
        main_cat_sub = data['main_cat_sub']
        sex = data['sex']
        color_selected = data['color_selected']
        req_color = []
        if color_selected:
            color_dict = data['color']
            req_color.append(color_dict['r'])
            req_color.append(color_dict['g'])
            req_color.append(color_dict['b'])

        shops = data['shops']
        brands = data['brands']
        max_price = float(data['max_price'])

        if brands[0] == 'All':
            id_list = db.session.query(Product).filter(
                ((Product.img_cats_ai_txt.any(main_cat_sub))
                 | (Product.spider_cat == main_cat_sub)
                 | (Product.img_cats_sc_txt.any(main_cat_sub)))
                & ((Product.img_cats_ai_txt.any(main_cat_top))
                   | (Product.spider_cat == main_cat_top)
                   | (Product.img_cats_sc_txt.any(main_cat_top)))
                & (Product.sex == sex)
                & (or_(*[Product.shop.ilike(shop) for shop in shops]))
                & (Product.price <= max_price)
            ).order_by(
                func.random()).limit(5000).all()

            if len(id_list) < 100:
                id_list = db.session.query(Product).filter(
                    ((Product.img_cats_ai_txt.any(main_cat_sub))
                     | (Product.spider_cat == main_cat_sub)
                     | (Product.img_cats_sc_txt.any(main_cat_sub)))
                    & (Product.sex == sex)
                    & (or_(*[Product.shop.ilike(shop) for shop in shops]))
                    & (Product.price <= max_price)
                ).order_by(
                    func.random()).limit(5000).all()

        else:
            id_list = db.session.query(Product).filter(
                ((Product.img_cats_ai_txt.any(main_cat_sub))
                 | (Product.spider_cat == main_cat_sub)
                 | (Product.img_cats_sc_txt.any(main_cat_sub)))
                & ((Product.img_cats_ai_txt.any(main_cat_top))
                   | (Product.spider_cat == main_cat_top)
                   | (Product.img_cats_sc_txt.any(main_cat_top)))
                & (Product.sex == sex)
                & (or_(*[Product.shop.ilike(shop) for shop in shops]))
                & (Product.price <= max_price)
                & (or_(*[Product.brand.ilike(brand) for brand in brands]))
            ).order_by(
                func.random()).limit(5000).all()

            if len(id_list) < 100:
                id_list = db.session.query(Product).filter(
                    ((Product.img_cats_ai_txt.any(main_cat_sub))
                     | (Product.spider_cat == main_cat_sub)
                     | (Product.img_cats_sc_txt.any(main_cat_sub)))
                    & (Product.sex == sex)
                    & (or_(*[Product.shop.ilike(shop) for shop in shops]))
                    & (Product.price <= max_price)
                    & (or_(*[Product.brand.ilike(brand) for brand in brands]))
                ).order_by(
                    func.random()).limit(5000).all()

        if color_selected:
            color_dist_list = []
            for prod_obj in id_list:
                color_prod_id = prod_obj.id
                color1_rgb = prod_obj.color_1
                color2_rgb = prod_obj.color_2
                color3_rgb = prod_obj.color_3

                distance_color_1 = int(
                    spatial.distance.euclidean(np.array(req_color, dtype=int), np.array(color1_rgb, dtype=int),
                                               w=None))
                distance_color_2 = int(
                    spatial.distance.euclidean(np.array(req_color, dtype=int), np.array(color2_rgb, dtype=int),
                                               w=None))
                distance_color_3 = int(
                    spatial.distance.euclidean(np.array(req_color, dtype=int), np.array(color3_rgb, dtype=int),
                                               w=None))

                color_dist = int((distance_color_1 + distance_color_2 + distance_color_3) / 3)

                item_obj = {
                    'id': color_prod_id,
                    'color_distance': color_dist
                }

                color_dist_list.append(item_obj)

            # Closest colors at top
            sorted_color_list = sorted(color_dist_list, key=itemgetter('color_distance'))
            top_color_list = sorted_color_list[0:100]

        else:
            shuffle(id_list)

            random_list = []
            counter = 0
            for prod_obj in id_list:
                counter += 1

                if counter < 100:
                    prod_id = prod_obj.id
                    item_obj = {
                        'id': prod_id
                    }

                    random_list.append(item_obj)

            top_color_list = random_list

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        result_list = []
        for obj in top_color_list:
            result_obj_id = obj['id']
            prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        # Make it HTTP friendly
        res = jsonify(res=result_list)
        # print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)
