import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask import render_template, request, jsonify
import string
from sqlalchemy import func, or_
import aiohttp
from get_features import get_features
from marshmallow_schema import LoadingContentSchema, ImagesFullWomenASchema, ImagesFullMenASchema, ProductsWomenASchema, ProductsMenASchema
from db_commit import image_commit, product_commit, insta_mention_commit
from db_search import search_similar_images, search_from_upload, db_text_search, db_test_search
from db_wardrobe import db_add_look, db_remove_look, db_get_looks, db_add_outfit, db_remove_outfit, db_rename_look
from db_recommend import recommend_similar_tags, recommend_from_random
from db_deals import get_deals
from send_email import password_reset_email
import transformation.cat_transform as cat_transformation
import transformation.enc_transform as enc_transformation
import transformation.brand_transform as brand_transformation
import transformation.skinny_transform as skinny_transformation
import transformation.preserve_faves_transform as preserve_transform
import data.cats as cats
from hashlib import sha256
import random

application = app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, ImagesFullWomenA, ImagesFullMenA, ImagesSkinnyWomenA, ImagesSkinnyMenA, InstaMentions, LoadingContent, ProductsWomenA, ProductsMenA


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
                first_login=first_login,
                wardrobe=None,
                looks=None,
                pw_reset_token=None
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


@app.route('/api/pw_reset_token', methods=['POST'])
def pw_reset_token():
    if request.method == 'POST':
        data = request.get_json(force=True)
        pw = data['pw']
        email = data['email']
        print(email)
        print(pw)

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(pw):
            return json.dumps(False)
        else:
            rand_string = ''.join(random.choice(string.ascii_letters) for m in range(10))
            token = sha256(rand_string.encode('utf-8')).hexdigest()
            user.pw_reset_token = token
            db.session.commit()
            print(token)
            return json.dumps({
                'token': token
            })


@app.route('/api/pw_reset', methods=['POST'])
def pw_reset():
    if request.method == 'POST':
        data = request.get_json(force=True)
        token = data['token']
        email = data['email']
        new_pw = data['new_pw']

        user = User.query.filter_by(email=email).first()

        if user is None:
            print('incorrect email')
            return json.dumps({
                'res': 'incorrect email'
            })
        else:
            if token != user.pw_reset_token:
                print('invalid token')
                return json.dumps({
                    'res': 'invalid token'
                })
            else:
                # db.session.query().filter(User.email == email).update({'password': new_pw})
                # user.password = new_pw
                user.password_hash = user.set_password(new_pw)
                user.pw_reset_token = None
                db.session.commit()
                print('success')
                return json.dumps({
                    'res': 'success'
                })


@app.route('/api/pw_reset_email', methods=['POST'])
def pw_reset_email():
    if request.method == 'POST':
        data = request.get_json(force=True)

        response = password_reset_email(db, User, data)

        return response


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


# @app.route("/api/insta_pics", methods=['GET'])
# def insta_pics():
#     if request.method == 'GET':
#         email = request.args.get('email')
#         user = User.query.filter_by(email=email).first()
#         insta_username = user.insta_username
#
#         if insta_username is None:
#             res = jsonify(res=None, insta_username=None)
#             return res
#         else:
#             insta_pics = db.session.query(InstaMentions).filter((InstaMentions.mention_username == insta_username)).all()
#
#             result_list = []
#             for insta_pic in insta_pics:
#                 insta_serial = InstaMentionSchema().dump(insta_pic)
#                 result_list.append(insta_serial)
#
#             res = jsonify(res=result_list, insta_username=insta_username)
#
#             return res


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

        db_tables = data['db_tables']
        if db_tables == 'women_a':
            upload_response = image_commit(db, ImagesFullWomenA, ImagesSkinnyWomenA, data)
            return upload_response
        else:
            upload_response = image_commit(db, ImagesFullMenA, ImagesSkinnyMenA, data)
            return upload_response


# Upload new product object to database
@app.route("/api/commit_product", methods=['post'])
def commit_product():
    if request.method == 'POST':
        data = request.get_json(force=True)

        db_tables = data['db_tables']
        if db_tables == 'women_a':
            upload_response = product_commit(db, ProductsWomenA, data)
            return upload_response
        else:
            upload_response = product_commit(db, ProductsMenA, data)
            return upload_response


# # Upload new product image to database
# @app.route("/api/commit_image_v2", methods=['post'])
# def commit_image_v2():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         # print(str(data))
#
#         upload_response = image_commit_v2(db, ImagesV2, data)
#
#         return upload_response


# Upload new product image to database
@app.route("/api/transform_skinny", methods=['post'])
def transform_skinny():
    if request.method == 'POST':
        data = request.get_json(force=True)
        # print(str(data))
        #     SkinnyTransform

        req_response = skinny_transformation.SkinnyTransform().img_skinny_transform(
            db,
            ImagesFullWomenA,
            ImagesSkinnyWomenA,
            image_commit_v2_skinny,
            data
        )

        return req_response


# # Upload new product image to database
# @app.route("/api/transform_preserve_faves", methods=['post'])
# def transform_preserve_faves():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#
#         req_response = preserve_transform.PreserveFaves().preserve_faves_transform(
#             db,
#             ImagesFullWomenA,
#             ImagesV2,
#             ImagesSkinnyWomenA,
#             ImagesV2Skinny,
#             ProductsWomenA,
#             ProductsV2,
#             User,
#             data
#         )
#
#         return req_response


# # Upload new product object to database
# @app.route("/api/commit_product_v2", methods=['post'])
# def commit_product_v2():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#
#         # print(str(data))
#         upload_response = product_commit_v2(db, ProductsV2, data)
#
#         return upload_response


@app.route("/api/submit_instagram", methods=['post'])
def submit_instagram():
    if request.method == 'POST':
        data = request.get_json(force=True)

        # print(str(data))
        insta_submit_response = insta_mention_commit(db, InstaMentions, data)

        return insta_submit_response


# # Delete product
# @app.route("/api/delete", methods=['get'])
# def delete():
#     if request.method == 'GET':
#         img_hash = request.args.get('img_hash')
#         shop = request.args.get('shop')
#
#         if len(img_hash) > 0:
#             try:
#                 existing_product = Product.query.filter_by(img_hash=img_hash).first()
#             except:
#                 existing_product = None
#             if existing_product is not None:
#                 db.session.delete(existing_product)
#                 db.session.commit()
#                 return json.dumps(True)
#             else:
#                 return json.dumps(False)
#
#         if len(shop) > 0:
#             try:
#                 shop_products = db.session.query(Product).filter(Product.shop == 'Zalando').order_by(
#                     func.random()).all()
#                 db.session.delete(shop_products)
#                 db.session.commit()
#                 return json.dumps(True)
#             except:
#                 return json.dumps(False)


# Trigram search for products with a search string
@app.route("/api/text_search", methods=['get'])
def text_search():
    if request.method == 'GET':
        req_sex = request.args.get('sex')
        if req_sex == 'women':
            print('searching from WOMEN')
            res = db_text_search(request, db, ProductsWomenA, ImagesFullWomenA, ImagesSkinnyWomenA)
        else:
            res = db_text_search(request, db, ProductsMenA, ImagesFullMenA, ImagesSkinnyMenA)

        return res


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
        data = request.get_json(force=True)
        data = json.loads(data)
        req_sex = data['sex']
        if req_sex == 'women':
            results = search_from_upload(request, db, ImagesFullWomenA, ImagesSkinnyWomenA, ProductsWomenA)
        else:
            results = search_from_upload(request, db, ImagesFullMenA, ImagesSkinnyMenA, ProductsMenA)
        # Make it HTTP friendly
        res = jsonify(res=results)

        return res


# Search for similar products based on selected product
@app.route("/api/search_similar", methods=['POST'])
def search_similar():
    print('Search similar requested, request method', str(request.method))
    if request.method == 'POST':
        print('Calling search_similar_images')
        data = request.get_json(force=True)
        data = json.loads(data)
        req_sex = data['sex']
        if req_sex == 'women':
            search_results = search_similar_images(request, db, ImagesFullWomenA, ImagesSkinnyWomenA, ProductsWomenA)
            res = jsonify(res=search_results)
        else:
            search_results = search_similar_images(request, db, ImagesFullMenA, ImagesSkinnyMenA, ProductsMenA)
            res = jsonify(res=search_results)

        return res


@app.route("/api/test_search", methods=['POST'])
def test_search():
    print('Search similar requested, request method', str(request.method))
    if request.method == 'POST':
        print('Calling test_search')
        search_results = db_test_search(request, db, ImagesFullMenA, ImagesSkinnyMenA, ProductsMenA)

        # Make it HTTP friendly
        res = jsonify(res=search_results)

        return res


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


@app.route("/api/rename_look", methods=['POST'])
def rename_look():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        rename_look_response = db_rename_look(db, User, data)

        return rename_look_response


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
        sex = data['sex']
        if sex == 'women':
            add_outfit_response = db_add_outfit(db, User, ProductsWomenA, data)
        else:
            add_outfit_response = db_add_outfit(db, User, ProductsMenA, data)

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
        sex = data['sex']
        # print(prod_hashes)
        conditions = []
        prod_results = []
        if sex == 'women':
            for prod_hash in prod_hashes:
                conditions.append(
                    (ProductsWomenA.prod_id == prod_hash)
                )
            query = db.session.query(ProductsWomenA).filter(
                or_(*conditions)
            )
            query_results = query.all()
            for query_result in query_results:
                prod_serial = ProductsWomenASchema().dump(query_result)
                prod_results.append(prod_serial)

        else:
            for prod_hash in prod_hashes:
                conditions.append(
                    (ProductsMenA.prod_id == prod_hash)
                )
            query = db.session.query(ProductsMenA).filter(
                or_(*conditions)
            )
            query_results = query.all()
            for query_result in query_results:
                prod_serial = ProductSchemaV2().dump(query_result)
                prod_results.append(prod_serial)

        return json.dumps(prod_results)


@app.route("/api/get_prod_hash", methods=['POST'])
def get_prod_hash():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = json.loads(data)
        print(data)
        img_hash = data['img_hash']
        sex = data['sex']
        if sex == 'women':
            product = db.session.query(ProductsWomenA).filter(ProductsWomenA.image_hash.any(img_hash)).first()
        else:
            product = db.session.query(ProductsMenA).filter(ProductsMenA.image_hash.any(img_hash)).first()
        prod_id = product.prod_id
        print({'prod_id': prod_id})
        return json.dumps({'prod_id': prod_id})


@app.route("/api/recommend_tags", methods=['POST'])
def recommend_tags():
    if request.method == 'POST':
        data = request.get_json(force=True)
        req_sex = data['sex']
        if req_sex == 'women':
            suggestions = recommend_similar_tags(db, User, ProductsWomenA, data)
        else:
            suggestions = recommend_similar_tags(db, User, ProductsMenA, data)
        return suggestions


@app.route("/api/recommend_random", methods=['POST'])
def recommend_random():
    if request.method == 'POST':
        data = request.get_json(force=True)
        req_sex = data['sex']
        if req_sex == 'women':
            print('suggesting from women table')
            suggestions = recommend_from_random(db, ProductsWomenA, data)
        else:
            suggestions = recommend_from_random(db, ProductsMenA, data)

        return suggestions


@app.route("/api/recommend_deals", methods=['POST'])
def recommend_deals():
    if request.method == 'POST':
        data = request.get_json(force=True)
        sex = data['sex']

        if sex == 'women':
            suggestions = get_deals(db, ImagesSkinnyWomenA, ProductsWomenA, data)
        else:
            suggestions = get_deals(db, ImagesSkinnyMenA, ProductsMenA, data)

        return suggestions


@app.route("/api/get_image", methods=['POST'])
def get_image():
    if request.method == 'POST':
        data = request.get_json(force=True)
        img_hash = data['img_hash']
        sex = data['sex']

        if sex == 'women':
            query = db.session.query(ImagesFullWomenA).filter(ImagesFullWomenA.img_hash == img_hash)
            query_result = query.first()
            img_serial = ImagesFullWomenASchema().dump(query_result)
        else:
            query = db.session.query(ImagesFullMenA).filter(ImagesFullMenA.img_hash == img_hash)
            query_result = query.first()
            img_serial = ImageSchemaV2().dump(query_result)

        return json.dumps(img_serial)


@app.route("/api/cat_transform", methods=['POST'])
def cat_transform():
    if request.method == 'POST':
        data = request.get_json(force=True)

        req_response = cat_transformation.CatTransform().cat_transform(cats, db, ImagesFullMenA, data)

        return json.dumps(req_response)


@app.route("/api/cat_cleanse_transform", methods=['POST'])
def cat_cleanse_transform():
    if request.method == 'POST':
        data = request.get_json(force=True)

        req_response = cat_transformation.cat_clean_transform(cats, db, ImagesSkinnyWomenA, data)

        return json.dumps(req_response)


@app.route("/api/cat_fix_liu", methods=['POST'])
def cat_fix_liu():
    if request.method == 'POST':
        data = request.get_json(force=True)

        req_response = cat_transformation.cat_fix_liu(db, ImagesSkinnyWomenA, data)

        return json.dumps(req_response)


@app.route("/api/cat_transform_boohoo", methods=['POST'])
def cat_transform_boohoo():
    if request.method == 'POST':
        data = request.get_json(force=True)

        req_response = cat_transformation.cat_fix_boohoo(db, ImagesSkinnyWomenA, data, cats)

        return json.dumps(req_response)


@app.route("/api/enc_transform", methods=['POST'])
def enc_transform():
    if request.method == 'POST':
        data = request.get_json(force=True)

        req_response = enc_transformation.EncTransform().enc_dim_transform(db, ImagesFullMenA, data)

        return json.dumps(req_response)


@app.route("/api/brand_transform", methods=['POST'])
def brand_transform():
    if request.method == 'POST':
        data = request.get_json(force=True)

        req_response = brand_transformation.BrandTransform().add_brand_to_images(db, ImagesFullMenA, ProductsMenA, data)

        return json.dumps(req_response)


@app.route("/api/add_vgg16", methods=['POST'])
def add_vgg16():
    if request.method == 'POST':
        data = request.get_json(force=True)
        img_hash = data['img_hash']
        encoding_vgg16 = data['encoding_vgg16']
        try:
            existing_img = ImagesFullMenA.query.filter_by(img_hash=img_hash).first()
        except:
            existing_img = None

        if existing_img is None:
            return json.dumps({
                'response': 'not found'
            })
        else:
            existing_img.encoding_vgg16 = encoding_vgg16
            db.session.commit()
            return json.dumps({
                'response': 'SUCCESS'
            })


@app.route("/api/count_in_stock", methods=['GET'])
def count_in_stock():
    if request.method == 'GET':
        stock_aggr = db.session.query(ImagesFullMenA.in_stock, func.count(ImagesFullMenA.in_stock)).group_by(ImagesFullMenA.in_stock).all()

        return json.dumps({
            'response': stock_aggr
        })


@app.route("/api/count_vgg16", methods=['GET'])
def count_vgg16():
    if request.method == 'GET':
        vgg16_none_count = db.session.query(ImagesFullMenA).filter(ImagesFullMenA.encoding_vgg16 == None).count()

        return json.dumps({
            'null_count': vgg16_none_count
        })


@app.route("/api/count_all", methods=['GET'])
def count_all():
    if request.method == 'GET':
        # row_count = db.session.query(ProductsWomenA).count()
        row_count = db.session.query(ImagesSkinnyWomenA).count()
        # row_count = db.session.query(ImagesFullWomenA).count()

        return json.dumps({
            'row_count': row_count
        })


@app.route("/api/count_prod_brands", methods=['GET'])
def count_prod_brands():
    if request.method == 'GET':
        prod_brand_aggr = db.session.query(ProductsMenA.brand, func.count(ProductsMenA.brand)).group_by(ProductsMenA.brand).all()

        return json.dumps({
            'response': prod_brand_aggr
        })


@app.route("/api/add_loading_content", methods=['POST'])
def add_loading_content():
    if request.method == 'POST':
        data = request.get_json(force=True)
        content_type = data['content_type']
        content_text = data['content_text']
        content_image = data['content_image']
        timestamp = int(datetime.datetime.now().timestamp())

        content_submission = LoadingContent(
            content_type=content_type,
            content_date=timestamp,
            content_text=content_text,
            content_image=content_image
        )
        db.session.add(content_submission)
        db.session.commit()
        
        return json.dumps(True)


@app.route("/api/get_random_loading_content", methods=['GET'])
def get_random_loading_content():
    if request.method == 'GET':
        loading_content = db.session.query(LoadingContent).order_by(func.random()).limit(1).one()
        loading_content_serial = LoadingContentSchema().dumps(loading_content, many=False)

        return loading_content_serial


@app.route('/api/health', methods=['GET'])
def health():
    if request.method == 'GET':

        return json.dumps({
            'ok': 'ok'
        })


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)
