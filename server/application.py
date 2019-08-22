# from random import shuffle
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask import render_template, request, jsonify
# import scipy.spatial as spatial
# import numpy as np
# from operator import itemgetter
import string
from sqlalchemy import func, any_, or_
# import asyncio
import aiohttp
from get_features import get_features
from marshmallow_schema import ProductSchema, ProductsSchema, InstaMentionSchema, ImageSchema
from db_commit import image_commit, product_commit, insta_mention_commit
from db_search import search_similar_images, search_from_upload, db_text_search
from db_wardrobe import db_add_look, db_remove_look, db_get_looks, db_add_outfit, db_remove_outfit


application = app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Product, Products, Images, InstaMentions


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
        fb_id = data['fb_id']
        first_login = data['first_login']

        user = User.query.filter_by(email=email).first()

        # If no such email exists in DB create a new user submission
        if user is None:
            reg_submission = User(
                username=username,
                email=email,
                sex=sex,
                password=pwd,
                fb_id=fb_id,
                favorites_ids='',
                insta_username=None,
                first_login=first_login
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
            first_login = user.first_login


            # print(username)
            user_dict = {
                'user_id': user_id,
                'username': username,
                'favorites': favorites,
                'sex': sex,
                'email': user_email,
                'first_login': first_login
            }

            res = jsonify(auth=True, res=user_dict)

            return res


@app.route("/api/complete_first_login", methods=['POST'])
def complete_first_login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        # data = json.loads(data)
        user_email = data['email']

        user = User.query.filter_by(email=user_email).first()
        user.first_login = 0

        db.session.commit()
        
        return json.dumps(True)


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

                if len(prod_serial[0]) == 0:
                    new_prod_search = db.session.query(Products).filter((Products.prod_hash == img_hash)).first()
                    if new_prod_search is None:
                        new_prod_search = db.session.query(Products).filter(Products.img_hashes.any(img_hash)).first()
                        prod_serial = ProductsSchema().dump(new_prod_search)
                    else:
                        prod_serial = ProductsSchema().dump(new_prod_search)
                        
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

        result_list = []
        for img_hash in favs:
            prod_search = db.session.query(Product).filter((Product.img_hash == img_hash)).first()
            try:
                prod_serial = ProductSchema().dump(prod_search)

            except:
                new_prod_search = db.session.query(Products).filter((Products.prod_hash == img_hash)).first()
                if new_prod_search is None:
                    new_prod_search = db.session.query(Products).filter(Products.img_hashes.any(img_hash)).first()
                    prod_serial = ProductsSchema().dump(new_prod_search)
                else:
                    prod_serial = ProductsSchema().dump(new_prod_search)

            if len(prod_serial[0]) == 0:
                new_prod_search = db.session.query(Products).filter((Products.prod_hash == img_hash)).first()
                if new_prod_search is None:
                    new_prod_search = db.session.query(Products).filter(Products.img_hashes.any(img_hash)).first()
                    prod_serial = ProductsSchema().dump(new_prod_search)
                else:
                    prod_serial = ProductsSchema().dump(new_prod_search)

            result_list.append(prod_serial)

        res = jsonify(res=result_list)

        return res


@app.route("/api/insta_pics", methods=['GET'])
def insta_pics():
    if request.method == 'GET':
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first()
        insta_username = user.insta_username

        if insta_username is None:
            res = jsonify(res=None, insta_username=None)
            return res
        else:
            insta_pics = db.session.query(InstaMentions).filter((InstaMentions.mention_username == insta_username)).all()

            result_list = []
            for insta_pic in insta_pics:
                insta_serial = InstaMentionSchema().dump(insta_pic)
                result_list.append(insta_serial)

            res = jsonify(res=result_list, insta_username=insta_username)

            return res


@app.route("/api/save_insta_username", methods=['POST'])
def save_insta_username():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        user_email = data['email']
        insta_username = data['insta_username']

        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return jsonify(insta_username=False)

        else:
            user.insta_username = insta_username
            db.session.commit()

            return jsonify(insta_username=insta_username)


@app.route('/api/logout')
def logout():
    return json.dumps('OK')


# Upload new product image to database
@app.route("/api/commit_image", methods=['post'])
def commit_image():
    if request.method == 'POST':
        data = request.get_json(force=True)
        # print(str(data))

        upload_response = image_commit(db, Images, data)

        return upload_response


# Upload new product object to database
@app.route("/api/commit_product", methods=['post'])
def commit_product():
    if request.method == 'POST':
        data = request.get_json(force=True)

        # print(str(data))
        upload_response = product_commit(db, Products, data)

        return upload_response


# Upload new product object to database
@app.route("/api/submit_instagram", methods=['post'])
def submit_instagram():
    if request.method == 'POST':
        data = request.get_json(force=True)

        # print(str(data))
        insta_submit_response = insta_mention_commit(db, InstaMentions, data)

        return insta_submit_response


# Delete product
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


# Trigram search for products with a search string
@app.route("/api/text_search", methods=['get'])
def text_search():
    if request.method == 'GET':
        res = db_text_search(request, db, Products, Images)
        print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))

        return res


# # Search for products with a search string
# @app.route("/api/text", methods=['get'])
# def text():
#     if request.method == 'GET':
#
#         print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))
#
#         return res


# Return color, encoding and category predictions from uploaded image
@app.route("/api/img_features", methods=['POST'])
def img_features():
    if request.method == 'POST':
        if request.files.get("image"):
            post_image = request.files["image"].read()
            # Obtain features from all AI servers
            features = get_features(post_image)

            # Make it HTTP friendly
            res = jsonify(res=features)

            return res


# Return color, encoding and category predictions from uploaded image
@app.route("/api/search_from_image", methods=['POST'])
def search_from_image():
    if request.method == 'POST':

        results = search_from_upload(request, db, Images, Products)
        # print('Search from image results: ', str(results))
        # Make it HTTP friendly
        res = jsonify(res=results)

        return res


# Search for similar products based on selected product
@app.route("/api/search_similar", methods=['GET'])
def search_similar():
    print('Search similar requested, request method', str(request.method))
    if request.method == 'GET':
        print('Calling search_similar_images')
        search_results = search_similar_images(request, db, Images, Products)

        # Make it HTTP friendly
        res = jsonify(res=search_results)

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

#
# @app.route("/api/explorer_search", methods=['POST'])
# def explorer_search():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         data = json.loads(data)
#
#
#         # Make it HTTP friendly
#         res = jsonify(res=result_list)
#         # print(BColors.WARNING + 'Response: ' + BColors.ENDC + str(res))
#
#         return res


@app.route("/api/add_look", methods=['POST'])
def add_look():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        add_look_response = db_add_look(db, User, data)

        return add_look_response


@app.route("/api/remove_look", methods=['POST'])
def remove_look():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        remove_look_response = db_remove_look(db, User, data)

        return remove_look_response


@app.route("/api/get_looks", methods=['POST'])
def get_looks():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        # print(data)
        get_looks_response = db_get_looks(db, User, data)
        # print(get_looks_response)
        return get_looks_response


@app.route("/api/add_outfit", methods=['POST'])
def add_outfit():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        add_outfit_response = db_add_outfit(db, User, Products, data)

        return add_outfit_response


@app.route("/api/remove_outfit", methods=['POST'])
def remove_outfit():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        remove_outfit_response = db_remove_outfit(db, User, data)

        return remove_outfit_response


@app.route("/api/get_products", methods=['POST'])
def get_products():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        prod_hashes = data['prod_hashes']
        conditions = []
        for prod_hash in prod_hashes:
            conditions.append(
                (Products.prod_hash == prod_hash)
            )
        query = db.session.query(Products).filter(
            or_(*conditions)
        )
        query_results = query.all()
        prod_results = []
        for query_result in query_results:
            prod_serial = ProductsSchema().dump(query_result)
            prod_results.append(prod_serial)

        return json.dumps(prod_results)


@app.route("/api/get_prod_hash", methods=['POST'])
def get_prod_hash():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        img_hash = data['img_hash']
        prodduct = db.session.query(Products).filter(Products.img_hashes.any(img_hash)).first()
        prod_hash = prodduct.prod_hash

        return json.dumps({'prod_hash': prod_hash})


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)
