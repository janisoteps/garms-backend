from application import db
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class InstaMentions(db.Model):
    __tablename__ = 'instamentions'
    id = db.Column(db.Integer, primary_key=True)
    mention_username = db.Column(db.String, index=True)
    comment_id = db.Column(db.String)
    mention_timestamp = db.Column(db.String)
    media_id = db.Column(db.String)
    media_type = db.Column(db.String)
    media_url = db.Column(db.String)
    media_permalink = db.Column(db.String)
    owner_username = db.Column(db.String)

    def __init__(
            self,
            mention_username,
            comment_id,
            mention_timestamp,
            media_id,
            media_type,
            media_url,
            media_permalink,
            owner_username):
        self.mention_username = mention_username
        self.comment_id = comment_id
        self.mention_timestamp = mention_timestamp
        self.media_id = media_id
        self.media_type = media_type
        self.media_url = media_url
        self.media_permalink = media_permalink
        self.owner_username = owner_username

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.mention_username


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fb_id = db.Column(db.String, index=True, unique=True)
    favorites_ids = db.Column(ARRAY(db.String))
    sex = db.Column(db.String)
    insta_username = db.Column(db.String)

    def __init__(self, username, email, sex, password, fb_id, favorites_ids, insta_username):
        self.password_hash = self.set_password(password)
        self.username = username
        self.email = email
        self.sex = sex
        self.fb_id = fb_id
        self.favorites_ids = favorites_ids
        self.insta_username = insta_username

    def set_password(self, password):
        pwd_hash = generate_password_hash(password)
        return pwd_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        # return '<User {}>'.format(self.username)
        return '<id=[{}] username=#{}# favorites=${}$ sex=*{}* email=%{}%>'\
            .format(self.id, self.username, self.favorites_ids, self.sex, self.email)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), index=True, unique=True)
    prod_url = db.Column(db.String)
    name = db.Column(db.Text, index=True)
    description = db.Column(db.Text)
    brand = db.Column(db.Text, index=True)
    shop = db.Column(db.Text)
    date = db.Column(db.Integer)
    sex = db.Column(db.String)
    currency = db.Column(db.String)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    img_url = db.Column(db.String)  # Scraped image source
    img_urls = db.Column(ARRAY(db.String))  # The rest of the scraped images of this product
    spider_cat = db.Column(db.Text, index=True)  # Category obtained during scraping
    img_cats_ai_txt = db.Column(ARRAY(db.Text), index=True)  # Image categories assigned by AI analysis text format
    img_cats_sc_txt = db.Column(ARRAY(db.Text), index=True)  # Image categories from scraped name in text format
    color_name = db.Column(db.Text, index=True)  # Text color value from scraped resources
    color_512 = db.Column(ARRAY(db.Integer))  # Array of 512 integers describing image color in 3D RGB space
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    color_3 = db.Column(ARRAY(db.Integer))
    color_3_hex = db.Column(db.String)
    pca_256 = db.Column(ARRAY(db.Integer))  # Array of 256 integers from 0 to 32 to represent visual encoding
    siamese_64 = db.Column(ARRAY(db.Integer))  # Array of 64 integers from 0 to 32 to represent visual encoding
    pattern_256 = db.Column(ARRAY(db.Integer))  # Array of 256 integers from 0 to 32 to represent visual pattern

    def __init__(self,
                 img_hash,
                 prod_url,
                 name,
                 description,
                 brand,
                 shop,
                 date,
                 sex,
                 currency,
                 price,
                 sale,
                 saleprice,
                 img_url,
                 img_urls,
                 spider_cat,
                 img_cats_ai_txt,
                 img_cats_sc_txt,
                 color_name,
                 color_512,
                 color_1,
                 color_1_hex,
                 color_2,
                 color_2_hex,
                 color_3,
                 color_3_hex,
                 pca_256,
                 siamese_64,
                 pattern_256):

        self.img_hash = img_hash
        self.prod_url = prod_url
        self.name = name
        self.description = description
        self.brand = brand
        self.shop = shop
        self.date = date
        self.sex = sex
        self.currency = currency
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.img_url = img_url
        self.img_urls = img_urls
        self.spider_cat = spider_cat
        self.img_cats_ai_txt = img_cats_ai_txt
        self.img_cats_sc_txt = img_cats_sc_txt
        self.color_name = color_name
        self.color_512 = color_512
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.color_3 = color_3
        self.color_3_hex = color_3_hex
        self.pca_256 = pca_256
        self.siamese_64 = siamese_64
        self.pattern_256 = pattern_256

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class Products(db.Model):
    __tablename__ = 'mainproducts'
    id = db.Column(db.Integer, primary_key=True)
    prod_hash = db.Column(db.String(40), index=True, unique=True)
    prod_url = db.Column(db.String)
    name = db.Column(db.Text, index=True)
    description = db.Column(db.Text)
    brand = db.Column(db.Text, index=True)
    shop = db.Column(db.Text)
    date = db.Column(db.Integer)
    sex = db.Column(db.String)
    currency = db.Column(db.String)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    img_url = db.Column(db.String)  # Scraped image source
    img_urls = db.Column(ARRAY(db.String))  # The rest of the scraped images of this product
    img_hashes = db.Column(ARRAY(db.String(40)), index=True)
    spider_cat = db.Column(db.Text, index=True)  # Category obtained during scraping
    img_cats_sc_txt = db.Column(ARRAY(db.Text), index=True)  # Image categories from scraped name in text format

    def __init__(self,
                 prod_hash,
                 prod_url,
                 name,
                 description,
                 brand,
                 shop,
                 date,
                 sex,
                 currency,
                 price,
                 sale,
                 saleprice,
                 img_url,
                 img_urls,
                 img_hashes,
                 spider_cat,
                 img_cats_sc_txt):

        self.prod_hash = prod_hash
        self.prod_url = prod_url
        self.name = name
        self.description = description
        self.brand = brand
        self.shop = shop
        self.date = date
        self.sex = sex
        self.currency = currency
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.img_url = img_url
        self.img_urls = img_urls
        self.img_hashes = img_hashes
        self.spider_cat = spider_cat
        self.img_cats_sc_txt = img_cats_sc_txt

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class Images(db.Model):
    __tablename__ = 'images'

    __table_args__ = (
        db.Index('name_idx', 'name', postgresql_ops={'name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), index=True, unique=True)
    prod_url = db.Column(db.String)
    img_url = db.Column(db.String)  # Scraped image source
    name = db.Column('name', db.Text, index=True)
    description = db.Column(db.Text)
    brand = db.Column(db.Text, index=True)
    shop = db.Column(db.Text)
    date = db.Column(db.Integer)
    sex = db.Column(db.String)
    currency = db.Column(db.String)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    spider_cat = db.Column(db.Text, index=True)  # Category obtained during scraping
    img_cats_ai_txt = db.Column(ARRAY(db.Text), index=True)  # Image categories assigned by AI analysis text format
    img_cats_sc_txt = db.Column(ARRAY(db.Text), index=True)  # Image categories from scraped name in text format
    color_name = db.Column(db.Text, index=True)  # Text color value from scraped resources
    color_512 = db.Column(ARRAY(db.Float))  # Array of 512 integers describing image color in 3D RGB space
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    color_3 = db.Column(ARRAY(db.Integer))
    color_3_hex = db.Column(db.String)
    encoding_nocrop = db.Column(ARRAY(db.Integer))  # Xception no top from full size image
    encoding_crop = db.Column(ARRAY(db.Integer))  # VGG19 from layer -20 from cropped image
    encoding_squarecrop = db.Column(ARRAY(db.Integer))  # VGG19 from layer -20 from square cropped image

    def __init__(self,
                 img_hash,
                 prod_url,
                 img_url,
                 name,
                 description,
                 brand,
                 shop,
                 date,
                 sex,
                 currency,
                 price,
                 sale,
                 saleprice,
                 spider_cat,
                 img_cats_ai_txt,
                 img_cats_sc_txt,
                 color_name,
                 color_512,
                 color_1,
                 color_1_hex,
                 color_2,
                 color_2_hex,
                 color_3,
                 color_3_hex,
                 encoding_nocrop,
                 encoding_crop,
                 encoding_squarecrop):

        self.img_hash = img_hash
        self.prod_url = prod_url
        self.name = name
        self.description = description
        self.brand = brand
        self.shop = shop
        self.date = date
        self.sex = sex
        self.currency = currency
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.img_url = img_url
        self.spider_cat = spider_cat
        self.img_cats_ai_txt = img_cats_ai_txt
        self.img_cats_sc_txt = img_cats_sc_txt
        self.color_name = color_name
        self.color_512 = color_512
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.color_3 = color_3
        self.color_3_hex = color_3_hex
        self.encoding_nocrop = encoding_nocrop
        self.encoding_crop = encoding_crop
        self.encoding_squarecrop = encoding_squarecrop

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name
