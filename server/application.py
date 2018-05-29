# import random
import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
import scipy.spatial as spatial
import numpy as np
from marshmallow import Schema, fields
from operator import itemgetter
import string
from sqlalchemy import func, any_
import re
from color_text import color_check
import asyncio
import aiohttp

application = app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Product


# # # # # # # Marshmallow schemas


class ProductSchema(Schema):
    id = fields.Integer()
    img_hash = fields.String()
    name = fields.String()
    shop = fields.String()
    brand = fields.String()
    price = fields.Number()
    saleprice = fields.Number()
    currency = fields.String()
    sale = fields.Boolean()
    sex = fields.String()
    color_name = fields.String()  # Text color value from scraped resources
    img_url = fields.String()  # Scraped image source
    prod_url = fields.String()
    img_cats_ai = fields.List(
        fields.Integer())  # Image categories assigned by AI analysis turned from array to integer (0-49)
    img_cats_ai_txt = fields.List(fields.String())  # Image categories assigned by AI analysis text format
    nr1_cat_ai = fields.Integer()
    img_cats_sc = fields.List(
        fields.Integer())  # Image categories from scraped name turned from array to integer (0-137)
    img_cats_sc_txt = fields.List(fields.String())  # Image categories from scraped name in text format
    nr1_cat_sc = fields.Integer()
    color_1 = fields.List(fields.Integer())  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = fields.String()
    color_1_int = fields.String()  # the closest color approximation to 125 color cats in int
    color_2 = fields.List(fields.Integer())
    color_2_hex = fields.String()
    color_3 = fields.List(fields.Integer())
    color_3_hex = fields.String()
    siamese_64 = fields.List(fields.Integer())


# # # # # # # Functions


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


# # # # # # # API functions


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


@app.route("/api/register")
def register():
    return create_user()


@app.route('/api/authping', methods=['GET'])
def loginsess():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return json.dumps(True)
        else:
            return json.dumps(False)


@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print(str(request))
        data = request.get_json(force=True)
        email = data['email']
        pwd = data['pwd']
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(pwd):
            return json.dumps(False)
        login_user(user, remember=True)
        return json.dumps(True)


@app.route('/api/logout')
def logout():
    logout_user()
    return json.dumps('OK')


@app.route("/api/favs")
def favs():
    return 'Here will be favs'


# Upload new product to database
@app.route("/api/commit", methods=['post'])
def commit():
    if request.method == 'POST':
        data = request.get_json(force=True)

        print(str(data))

        img_hash = data['img_hash']
        name = data['name']
        shop = data['shop']
        brand = data['brand']
        price = data['price']
        saleprice = data['saleprice']
        currency = data['currency']
        sale = data['sale']
        sex = data['sex']
        color_name = data['color_name']
        img_url = data['img_url']
        prod_url = data['prod_url']
        img_cats_ai = data['img_cats_ai']
        img_cats_ai_txt = data['img_cats_ai_txt']
        nr1_cat_ai = data['nr1_cat_ai']
        img_cats_sc = data['img_cats_sc']
        img_cats_sc_txt = data['img_cats_sc_txt']
        nr1_cat_sc = data['nr1_cat_sc']
        color_1 = data['color_1']
        color_1_hex = data['color_1_hex']
        color_1_int = data['color_1_int']
        color_2 = data['color_2']
        color_2_hex = data['color_2_hex']
        color_3 = data['color_3']
        color_3_hex = data['color_3_hex']
        siamese_64 = data['siamese_64']

        product_submission = Product(
            img_hash=img_hash,
            name=name,
            shop=shop,
            brand=brand,
            price=price,
            saleprice=saleprice,
            currency=currency,
            sale=sale,
            sex=sex,
            color_name=color_name,
            img_url=img_url,
            prod_url=prod_url,
            img_cats_ai=img_cats_ai,
            img_cats_ai_txt=img_cats_ai_txt,
            nr1_cat_ai=nr1_cat_ai,
            img_cats_sc=img_cats_sc,
            img_cats_sc_txt=img_cats_sc_txt,
            nr1_cat_sc=nr1_cat_sc,
            color_1=color_1,
            color_1_hex=color_1_hex,
            color_1_int=color_1_int,
            color_2=color_2,
            color_2_hex=color_2_hex,
            color_3=color_3,
            color_3_hex=color_3_hex,
            siamese_64=siamese_64
        )

        try:
            existing_product = Product.query.filter_by(img_hash=img_hash).first()
        except:
            existing_product = None

        if existing_product is None:
            print('Adding a new product')
            db.session.add(product_submission)
            db.session.commit()
            return json.dumps(True)

        else:
            print('Updating existing product')
            existing_product.name = name
            existing_product.shop = shop
            existing_product.brand = brand
            existing_product.price = price
            existing_product.saleprice = saleprice
            existing_product.currency = currency
            existing_product.sale = sale
            existing_product.sex = sex
            existing_product.color_name = color_name
            existing_product.img_url = img_url
            existing_product.prod_url = prod_url
            existing_product.img_cats_ai = img_cats_ai
            existing_product.img_cats_ai_txt = img_cats_ai_txt
            existing_product.nr1_cat_ai = nr1_cat_ai
            existing_product.img_cats_sc = img_cats_sc
            existing_product.img_cats_sc_txt = img_cats_sc_txt
            existing_product.nr1_cat_sc = nr1_cat_sc
            existing_product.color_1 = color_1
            existing_product.color_1_hex = color_1_hex
            existing_product.color_1_int = color_1_int
            existing_product.color_2 = color_2
            existing_product.color_2_hex = color_2_hex
            existing_product.color_3 = color_3
            existing_product.color_3_hex = color_3_hex
            existing_product.siamese_64 = siamese_64

            db.session.commit()
            return json.dumps(True)


# Search for similar products based on selected product
@app.route("/api/search", methods=['get'])
def search():
    if request.method == 'GET':
        main_cat = request.args.get('main_cat')
        nr1_cat_ai = request.args.get('nr1_cat_ai')
        nr1_cat_sc = request.args.get('nr1_cat_sc')
        color_1 = request.args.get('color_1').strip('\'[]').split(',')
        # color_2 = request.args.get('color_2')
        siamese_64 = request.args.get('siamese_64').strip('\'[]').split(',')
        siamese_64 = [int(float(i)) for i in siamese_64]
        if color_1 is None:
            return json.dumps('BAD REQUEST')

        # Start off by doing the initial query looking for categories
        id_list = db.session.query(Product).filter(
            (Product.nr1_cat_ai == nr1_cat_ai) | (Product.nr1_cat_sc == nr1_cat_sc) | (Product.img_cats_sc_txt.any(main_cat))).order_by(func.random()).limit(
            1000).all()

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        # Build a list of ids and color distances from query product
        color_dist_list = []
        for prod_id in id_list:
            prod_id_str = str(prod_id)
            # Turn into list id, color and siamese encoding
            color_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]
            color1_rgb = re.search('(?<=color1=\[).{5,13}(?=\])', prod_id_str)[0]
            color1_rgb = color1_rgb.replace(" ", "").strip('\'[]')
            color1_rgb = color1_rgb.split(',')
            color1_rgb = [int(i) for i in color1_rgb]

            print('Color RGB: ', str(color1_rgb))

            try:
                image_prod_name = re.search('(?<=name=@).{5,80}(?=@)', prod_id_str)[0]
            except:
                image_prod_name = None

            if image_prod_name is not None:
                image_prod_name = image_prod_name.strip('\'[]')
                image_prod_name_arr = image_prod_name.lower().split(' ')

                if main_cat in image_prod_name_arr:
                    # Use euclidean distance to measure how similar the color is in RGB space
                    # And then to measure how close the siamese encoding is 64 dimensional space
                    distance_color = int(
                        spatial.distance.euclidean(np.array(color_1, dtype=int), np.array(color1_rgb, dtype=int), w=None))

                    print(BColors.OKBLUE + 'Color distance: ' + BColors.ENDC + str(distance_color))

                    item_obj = {'id': color_prod_id, 'color_distance': distance_color, 'prod_string': prod_id_str}

                    color_dist_list.append(item_obj)

        # Closest colors at top
        sorted_color_list = sorted(color_dist_list, key=itemgetter('color_distance'))

        top_color_list = sorted_color_list[0:250]

        siamese_dist_list = []
        for prod_obj in top_color_list:
            test_siamese_64 = re.search('(?<=siam=\[).+(?=\])', prod_obj['prod_string'])[0]
            test_siamese_64 = test_siamese_64.replace(" ", "").strip('\'[]')
            # print('Siamese before splitting: ', str(test_siamese_64))
            test_siamese_64 = test_siamese_64.split(',')
            test_siamese_64 = [int(float(i)) for i in test_siamese_64]

            distance_siam = int(
                spatial.distance.euclidean(np.array(siamese_64, dtype=int), np.array(test_siamese_64, dtype=int),
                                           w=None))

            print(BColors.OKGREEN + 'Siamese distance: ' + BColors.ENDC + str(distance_siam))

            distance = prod_obj['color_distance'] + distance_siam

            item_obj = {'id': prod_obj['id'], 'distance': distance}

            siamese_dist_list.append(item_obj)

        # Closest colors at top
        sorted_list = sorted(siamese_dist_list, key=itemgetter('distance'))

        # Only top results are returned
        top_list = sorted_list[0:30]

        result_list = []
        for obj in top_list:
            result_obj_id = obj['id']
            prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        # serialized = product_schema.dump(query)
        # result = product_schema.dump(query)
        # names = query.return_name()
        # for match in cat_match_list:
        #     dist = sc.spatial.distance.euclidean(np.array(match.color_1), np.array(color_1), w=None)

        # print(BColors.WARNING + 'Marshmallow Result: ' + BColors.ENDC + str(result_list))
        # response_list = list(str(query))
        # Make it HTTP friendly
        res = jsonify(res=result_list)
        # print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


# Search for products with a search string
@app.route("/api/text", methods=['get'])
def text():
    if request.method == 'GET':
        search_string = request.args.get('string')

        print('Text search with string: ', str(search_string))
        # cleaned_string = search_string.translate(' ', "!@£$%^&*()<>?/|~`.,:;#+=_")

        string_list = search_string.strip().lower().split()
        print('string list', str(string_list))
        linking_words = ['with', 'on', 'under', 'over', 'at', 'like', 'in', 'for', 'as', 'after']

        string_list_clean = [e for e in string_list if e not in linking_words]

        # string_list = cleaned_string.split()
        # print(string_list_clean)
        color_word_dict = color_check(string_list_clean)

        print(color_word_dict)
        word_list = color_word_dict['words']
        color_list = color_word_dict['colors']

        # id_list = db.session.query(Product).filter(
        #     (func.lower(Product.name).contains(word_list[0]))).order_by(
        #     func.random()).limit(50).all()

        id_list = []
        if 2 > len(word_list) > 0 and len(color_list) > 0:
            print('1 word and is color')
            id_list += db.session.query(Product).filter((func.lower(Product.name).contains(word_list[-1])) & (
                func.lower(Product.color_name).contains(color_list[0]))).order_by(func.random()).limit(50).all()
            # id_list += db.session.query(Product).filter((Product.img_cats_sc_txt.contains(word_list[0])) & (
            #     Product.color_name.contains(color_list[0]))).order_by(func.random()).limit(50).all()

        elif 3 > len(word_list) > 1 and len(color_list) > 0:
            print('2 words and is color')
            id_list += db.session.query(Product).filter((func.lower(Product.name).contains(word_list[-1])) & (
                func.lower(Product.name).contains(word_list[1])) & (
                                                            func.lower(Product.color_name).contains(
                                                                color_list[0]))).order_by(func.random()).limit(50).all()

        elif 3 > len(word_list) > 1:
            print('2 words, no color')
            id_list += db.session.query(Product).filter((func.lower(Product.name).contains(word_list[0])) & (
                func.lower(Product.name).contains(word_list[1]))).order_by(func.random()).limit(50).all()

        elif 4 > len(word_list) > 2:
            print('3 words, no color')
            id_list += db.session.query(Product).filter((func.lower(Product.name).contains(word_list[0])) & (
                func.lower(Product.name).contains(word_list[1])) & (
                                                            func.lower(Product.name).contains(word_list[2]))).order_by(
                func.random()).limit(50).all()
            # word_len = len(word_list)
            # for i in range(0, word_len):
            #     id_list += db.session.query(Product).filter(
            #         (func.lower(Product.name).contains(word_list[i]))).order_by(
            #         func.random()).limit(30).all()
        elif 2 > len(word_list) > 0:
            print('1 word, no color')
            id_list += db.session.query(Product).filter((func.lower(Product.name).contains(word_list[-1]))).order_by(func.random()).limit(50).all()

        elif len(color_list) > 0:
            print('only color')
            color_len = len(color_list)
            for k in range(0, color_len):
                id_list += db.session.query(Product).filter(
                    (func.lower(Product.color_name).contains(color_list[k]))).order_by(
                    func.random()).limit(30).all()

        else:
            return json.dumps('BAD REQUEST')

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        result_list = []
        for prod_id in id_list:
            prod_id_str = str(prod_id)
            text_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]
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


@app.route("/api/image", methods=['POST'])
def image():
    if request.method == 'POST':
        if request.files.get("image"):
            # Get the image file from client post request
            post_image = request.files["image"].read()
            print('Got image search request')
            # Two AI APIs have been successfully built
            color_api = 'http://34.242.36.122/api/color'
            cat_api = 'http://34.243.167.38/api/cats'
            api_urls = [color_api, cat_api]

            tasks = [send_file(url, post_image) for url in api_urls]
            loop = asyncio.get_event_loop()
            # Gather responses from APIs using asyncio
            color_response, cat_response = loop.run_until_complete(asyncio.gather(*tasks))

            img_cats_ai = json.loads(cat_response)['res']['img_cats_ai']
            # If AI has recognized any categories, retrieve a random selection of n prods from db with that category
            if len(img_cats_ai) > 0:
                nr1_cat_ai = img_cats_ai[0]
                id_list = db.session.query(Product).filter((Product.nr1_cat_ai == nr1_cat_ai)).order_by(func.random()).limit(500).all()
            else:
                return json.dumps('Not recognized')

            # Declare Marshmallow schema so that SqlAlchemy object can be serialized
            product_schema = ProductSchema()

            # Go through the 1000 prods returned from db and order by color sim, then return top 30
            color_1 = json.loads(color_response)['res']['color_1']
            dist_list = []
            for prod_id in id_list:
                prod_id_str = str(prod_id)
                image_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]

                color1_rgb = re.search('(?<=color1=\[).{5,13}(?=\])', prod_id_str)[0]
                color1_rgb = color1_rgb.replace(" ", "").strip('\'[]')
                color1_rgb = color1_rgb.split(',')
                color1_rgb = [int(i) for i in color1_rgb]

                distance_color = int(
                    spatial.distance.euclidean(np.array(color_1, dtype=int), np.array(color1_rgb, dtype=int), w=None))

                print(BColors.OKBLUE + 'Color distance: ' + BColors.ENDC + str(distance_color))

                item_obj = {'id': image_prod_id, 'distance': distance_color}

                dist_list.append(item_obj)

            # Closest colors at top
            sorted_list = sorted(dist_list, key=itemgetter('distance'))

            # Only top results are returned
            top_list = sorted_list[0:30]

            # Now return db fields of these top similar prods to client
            result_list = []
            for obj in top_list:
                result_obj_id = obj['id']
                prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
                prod_serial = product_schema.dump(prod_search)
                result_list.append(prod_serial)

            # Make it HTTP friendly
            res = jsonify(res=result_list)

            # res = jsonify(res=response)
            print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

            return res


@app.route("/api/color", methods=['POST'])
def color():
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


@app.route("/api/colorcat", methods=['POST'])
def colorcat():
    if request.method == 'POST':
        if request.files.get("image"):
            post_image = request.files["image"].read()
            print('Got color and category predict request')

            # Two AI APIs have been successfully built
            color_api = 'http://34.242.36.122/api/color'
            cat_api = 'http://34.243.167.38/api/cats'
            siamese_api = 'http://34.248.44.245:5000/api/encoding'

            api_urls = [color_api, cat_api, siamese_api]

            tasks = [send_file(url, post_image) for url in api_urls]
            loop = asyncio.get_event_loop()
            # Gather responses from APIs using asyncio
            color_response, cat_response, siamese_response = loop.run_until_complete(asyncio.gather(*tasks))

            if np.isnan(float(json.loads(siamese_response)['res']['siamese_64'][0])):
                siamese_retry_task = send_file(siamese_api, post_image)
                siamese_retry_response = loop.run_until_complete(siamese_retry_task)
                siamese_response = siamese_retry_response

            img_cats_ai_txt = json.loads(cat_response)['res']['img_cats_ai_txt']
            color_1 = json.loads(color_response)['res']['color_1']
            color_1_hex = json.loads(color_response)['res']['color_1_hex']
            color_2 = json.loads(color_response)['res']['color_2']
            color_2_hex = json.loads(color_response)['res']['color_2_hex']
            color_3 = json.loads(color_response)['res']['color_3']
            color_3_hex = json.loads(color_response)['res']['color_3_hex']
            siamese_64 = json.loads(siamese_response)['res']['siamese_64']

            results = {
                'img_cats_ai_txt': img_cats_ai_txt,
                'colors': {
                    'color_1': color_1,
                    'color_1_hex': color_1_hex,
                    'color_2': color_2,
                    'color_2_hex': color_2_hex,
                    'color_3': color_3,
                    'color_3_hex': color_3_hex
                },
                'siamese_64': siamese_64
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
        siamese_64 = request.args.get('siamese_64').strip('\'[]').split(',')
        siamese_64 = [int(float(i)) for i in siamese_64]

        id_list = db.session.query(Product).filter(Product.img_cats_sc_txt.any(cat_ai_txt)).order_by(
            func.random()).limit(1000).all()

        color_dist_list = []
        for prod_id in id_list:
            prod_id_str = str(prod_id)
            image_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]

            color1_rgb = re.search('(?<=color1=\[).{5,13}(?=\])', prod_id_str)[0]
            color1_rgb = color1_rgb.replace(" ", "").strip('\'[]')
            color1_rgb = color1_rgb.split(',')
            color1_rgb = [int(i) for i in color1_rgb]

            try:
                image_prod_name = re.search('(?<=name=@).{5,80}(?=@)', prod_id_str)[0]
            except:
                image_prod_name = None

            if image_prod_name is not None:
                image_prod_name = image_prod_name.strip('\'[]')
                image_prod_name_arr = image_prod_name.lower().split(' ')

                print('name array: ', str(image_prod_name_arr))

                distance_color = int(
                    spatial.distance.euclidean(np.array(color_rgb, dtype=int), np.array(color1_rgb, dtype=int),
                                               w=None))

                if cat_ai_txt in image_prod_name_arr:
                    print(BColors.OKBLUE + 'Color distance: ' + BColors.ENDC + str(distance_color))

                    item_obj = {'id': image_prod_id, 'distance': distance_color, 'prod_string': prod_id_str}

                    color_dist_list.append(item_obj)

        # Closest colors at top
        color_sorted_list = sorted(color_dist_list, key=itemgetter('distance'))
        top_color_list = color_sorted_list[0:200]

        # Find most similar as per close cropped siamese encoding euclidean distance
        siamese_dist_list = []
        for prod_obj in top_color_list:
            test_siamese_64 = re.search('(?<=siam=\[).+(?=\])', prod_obj['prod_string'])[0]
            test_siamese_64 = test_siamese_64.replace(" ", "").strip('\'[]')
            # print('Siamese before splitting: ', str(test_siamese_64))
            test_siamese_64 = test_siamese_64.split(',')
            test_siamese_64 = [int(float(i)) for i in test_siamese_64]

            distance_siam = int(
                spatial.distance.euclidean(np.array(siamese_64, dtype=int), np.array(test_siamese_64, dtype=int),
                                           w=None))

            print(BColors.OKGREEN + 'Siamese distance: ' + BColors.ENDC + str(distance_siam))

            # distance = prod_obj['color_distance'] + distance_siam
            distance = distance_siam

            item_obj = {'id': prod_obj['id'], 'distance': distance}

            siamese_dist_list.append(item_obj)

        # Only top results are returned
        top_list = siamese_dist_list[0:30]

        # Declare Marshmallow schema so that SqlAlchemy object can be serialized
        product_schema = ProductSchema()

        # Now return db fields of these top similar prods to client
        result_list = []
        for obj in top_list:
            result_obj_id = obj['id']
            prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
            prod_serial = product_schema.dump(prod_search)
            result_list.append(prod_serial)

        # Make it HTTP friendly
        res = jsonify(res=result_list)

        # res = jsonify(res=response)
        print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


@app.route("/api/colorimage", methods=['POST'])
def colorimage():
    if request.method == 'POST':
        if request.files.get("image"):
            post_image = request.files["image"].read()
            cat_api = 'http://34.243.167.38/api/cats'
            post_color = request.form['color'].strip('\'[]').split(',')

            task = send_file(cat_api, post_image)

            loop = asyncio.get_event_loop()

            # Gather response from API using asyncio
            cat_response = loop.run_until_complete(task)

            img_cats_ai = json.loads(cat_response)['res']['img_cats_ai']
            img_cats_ai_txt = json.loads(cat_response)['res']['img_cats_ai_txt']

            # If AI has recognized any categories, retrieve a random selection of n prods from db with that category
            if len(img_cats_ai) > 0:
                # nr1_cat_ai = img_cats_ai[0]
                nr1_cat_ai_txt = img_cats_ai_txt[0]
                # id_list = db.session.query(Product).filter((Product.nr1_cat_ai == nr1_cat_ai)).order_by(
                #     func.random()).limit(500).all()
                id_list = db.session.query(Product).filter(Product.img_cats_sc_txt.any(nr1_cat_ai_txt)).order_by(
                    func.random()).limit(500).all()
            else:
                return json.dumps(False)

            dist_list = []
            for prod_id in id_list:
                prod_id_str = str(prod_id)
                image_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]

                color1_rgb = re.search('(?<=color1=\[).{5,13}(?=\])', prod_id_str)[0]
                color1_rgb = color1_rgb.replace(" ", "").strip('\'[]')
                color1_rgb = color1_rgb.split(',')
                color1_rgb = [int(i) for i in color1_rgb]

                try:
                    image_prod_name = re.search('(?<=name=@).{5,80}(?=@)', prod_id_str)[0]
                except:
                    image_prod_name = None

                if image_prod_name is not None:
                    image_prod_name = image_prod_name.strip('\'[]')
                    image_prod_name_arr = image_prod_name.lower().split(' ')

                    print('name array: ', str(image_prod_name_arr))

                    distance_color = int(
                        spatial.distance.euclidean(np.array(post_color, dtype=int), np.array(color1_rgb, dtype=int), w=None))

                    if nr1_cat_ai_txt in image_prod_name_arr:
                        print(BColors.OKBLUE + 'Color distance: ' + BColors.ENDC + str(distance_color))

                        item_obj = {'id': image_prod_id, 'distance': distance_color}

                        dist_list.append(item_obj)

            # Closest colors at top
            sorted_list = sorted(dist_list, key=itemgetter('distance'))

            # Only top results are returned
            top_list = sorted_list[0:30]

            # Declare Marshmallow schema so that SqlAlchemy object can be serialized
            product_schema = ProductSchema()

            # Now return db fields of these top similar prods to client
            result_list = []
            for obj in top_list:
                result_obj_id = obj['id']
                prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
                prod_serial = product_schema.dump(prod_search)
                result_list.append(prod_serial)

            # Make it HTTP friendly
            res = jsonify(res=result_list)

            # res = jsonify(res=response)
            print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

            return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)

# if root_url == developer_url:
#     if __name__ == "__main__":
#         app.run(host='0.0.0.0', threaded=True, port=3000)
