from application import db
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from application import login
import scipy.spatial as spatial
import numpy as np


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fb_id = db.Column(db.String, index=True, unique=True)
    favorites_ids = db.Column(ARRAY(db.String))

    def __init__(self, username, email, password, fb_id, favorites_ids):
        self.password_hash = self.set_password(password)
        self.username = username
        self.email = email
        self.fb_id = fb_id
        self.favorites_ids = favorites_ids

    def set_password(self, password):
        pwd_hash = generate_password_hash(password)
        return pwd_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), index=True, unique=True)
    name = db.Column(db.String)
    shop = db.Column(db.String)
    brand = db.Column(db.String)
    price = db.Column(db.Float)
    saleprice = db.Column(db.Float)
    currency = db.Column(db.String)
    sale = db.Column(db.Boolean)
    sex = db.Column(db.String)
    color_name = db.Column(db.String)  # Text color value from scraped resources
    img_url = db.Column(db.String)  # Scraped image source
    prod_url = db.Column(db.String)
    img_cats_ai = db.Column(ARRAY(db.Integer))  # Image categories assigned by AI analysis turned from array to integer (0-49)
    img_cats_ai_txt = db.Column(ARRAY(db.String))  # Image categories assigned by AI analysis text format
    nr1_cat_ai = db.Column(db.Integer, index=True)
    img_cats_sc = db.Column(ARRAY(db.Integer))  # Image categories from scraped name turned from array to integer (0-137)
    img_cats_sc_txt = db.Column(ARRAY(db.String))  # Image categories from scraped name in text format
    nr1_cat_sc = db.Column(db.Integer, index=True)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_1_int = db.Column(db.Integer, index=True)  # the closest color approximation to 125 color cats in int
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    siamese_64 = db.Column(ARRAY(db.Integer))  # Array of 64 integers from 0 to 32 to represent visual encoding

    def __init__(self,
                 img_hash,
                 name,
                 shop,
                 brand,
                 price,
                 saleprice,
                 currency,
                 sale,
                 sex,
                 color_name,
                 img_url,
                 prod_url,
                 img_cats_ai,
                 img_cats_ai_txt,
                 nr1_cat_ai,
                 img_cats_sc,
                 img_cats_sc_txt,
                 nr1_cat_sc,
                 color_1,
                 color_1_hex,
                 color_1_int,
                 color_2,
                 color_2_hex,
                 siamese_64):

        self.img_hash = img_hash
        self.name = name
        self.shop = shop
        self.brand = brand
        self.price = price
        self.saleprice = saleprice
        self.currency = currency
        self.sale = sale
        self.sex = sex
        self.color_name = color_name
        self.img_url = img_url
        self.prod_url = prod_url
        self.img_cats_ai = img_cats_ai
        self.img_cats_ai_txt = img_cats_ai_txt
        self.nr1_cat_ai = nr1_cat_ai
        self.img_cats_sc = img_cats_sc
        self.img_cats_sc_txt = img_cats_sc_txt
        self.nr1_cat_sc = nr1_cat_sc
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_1_int = color_1_int
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.siamese_64 = siamese_64

    # def find_similar(self, img_cats_ai, img_cats_ai_txt, nr1_cat_ai, color_1, color_2, siamese_64):

    def __repr__(self):
        return '<id=[{}] color1={} siam=[{}]>'.format(self.id, self.color_1, self.siamese_64)

    def return_name(self):
        return self.name

    def color_dist(self, color_array):
        own_color = self.color_1
        print('Query color: ', str(color_array))
        # print()
        distance = int(spatial.distance.euclidean(np.array(color_array, dtype=int), np.array(own_color, dtype=int), w=None))
        print('Distance: ', str(distance))
        return '{}'.format(distance)
        # return self.num > n - 5 and self.num <= n + 5