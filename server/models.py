from application import db
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList


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
    user_hash = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fb_id = db.Column(db.String, index=True, unique=True)
    favorites_ids = db.Column(ARRAY(db.String))
    sex = db.Column(db.String)
    insta_username = db.Column(db.String)
    first_login = db.Column(db.Integer)
    wardrobe = db.Column(MutableList.as_mutable(JSONB))
    looks = db.Column(MutableList.as_mutable(JSONB))
    pw_reset_token = db.Column(db.String(64))

    def __init__(
            self,
            user_hash,
            username,
            email,
            sex,
            password,
            fb_id,
            favorites_ids,
            insta_username,
            first_login,
            wardrobe,
            looks,
            pw_reset_token
    ):
        self.password_hash = self.set_password(password)
        self.user_hash = user_hash
        self.username = username
        self.email = email
        self.sex = sex
        self.fb_id = fb_id
        self.favorites_ids = favorites_ids
        self.insta_username = insta_username
        self.first_login = first_login
        self.wardrobe = wardrobe
        self.looks = looks
        self.pw_reset_token = pw_reset_token

    def set_password(self, password):
        pwd_hash = generate_password_hash(password)
        return pwd_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        # return '<User {}>'.format(self.username)
        return '<id=[{}] username=#{}# favorites=${}$ sex=*{}* email=%{}%>' \
            .format(self.id, self.username, self.favorites_ids, self.sex, self.email)


class ImagesSkinnyWomenB(db.Model):
    __tablename__ = 'images_skinny_women_b'

    __table_args__ = (
        db.Index('images_skinny_women_b_name_idx', 'img_skinny_name', postgresql_ops={'img_skinny_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer)
    img_hash = db.Column(db.String(40), index=True, unique=True, primary_key=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_skinny_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String), index=True)  # new
    color_cats = db.Column(ARRAY(db.String), index=True)  # new
    style_cats = db.Column(ARRAY(db.String), index=True)
    material_cats = db.Column(ARRAY(db.String), index=True)
    attribute_cats = db.Column(ARRAY(db.String), index=True)
    length_cats = db.Column(ARRAY(db.String), index=True)  # new
    filter_cats = db.Column(ARRAY(db.String), index=True)
    all_cats = db.Column(ARRAY(db.String), index=True)
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_2 = db.Column(ARRAY(db.Integer))
    color_3 = db.Column(ARRAY(db.Integer))
    color_4 = db.Column(ARRAY(db.Integer))
    color_5 = db.Column(ARRAY(db.Integer))
    color_6 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 color_1,
                 color_2,
                 color_3,
                 color_4,
                 color_5,
                 color_6,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5
        self.color_6 = color_6
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesSkinnyWomenC(db.Model):
    __tablename__ = 'images_skinny_women_c'

    __table_args__ = (
        db.Index('images_skinny_women_c_name_idx', 'img_skinny_name', postgresql_ops={'img_skinny_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer)
    img_hash = db.Column(db.String(40), index=True, unique=True, primary_key=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_skinny_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String), index=True)
    color_cats = db.Column(ARRAY(db.String), index=True)
    style_cats = db.Column(ARRAY(db.String), index=True)
    material_cats = db.Column(ARRAY(db.String), index=True)
    attribute_cats = db.Column(ARRAY(db.String), index=True)
    length_cats = db.Column(ARRAY(db.String), index=True)
    filter_cats = db.Column(ARRAY(db.String), index=True)
    all_cats = db.Column(ARRAY(db.String), index=True)
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_2 = db.Column(ARRAY(db.Integer))
    color_3 = db.Column(ARRAY(db.Integer))
    color_4 = db.Column(ARRAY(db.Integer))
    color_5 = db.Column(ARRAY(db.Integer))
    color_6 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 color_1,
                 color_2,
                 color_3,
                 color_4,
                 color_5,
                 color_6,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5
        self.color_6 = color_6
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesSkinnyMenB(db.Model):
    __tablename__ = 'images_skinny_men_b'

    __table_args__ = (
        db.Index('images_skinny_men_b_name_idx', 'img_skinny_name', postgresql_ops={'img_skinny_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer)
    img_hash = db.Column(db.String(40), index=True, unique=True, primary_key=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_skinny_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))  # new
    color_cats = db.Column(ARRAY(db.String))  # new
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))  # new
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String), index=True)
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_2 = db.Column(ARRAY(db.Integer))
    color_3 = db.Column(ARRAY(db.Integer))
    color_4 = db.Column(ARRAY(db.Integer))
    color_5 = db.Column(ARRAY(db.Integer))
    color_6 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 color_1,
                 color_2,
                 color_3,
                 color_4,
                 color_5,
                 color_6,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5
        self.color_6 = color_6
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesSkinnyMenC(db.Model):
    __tablename__ = 'images_skinny_men_c'

    __table_args__ = (
        db.Index('images_skinny_men_c_name_idx', 'img_skinny_name', postgresql_ops={'img_skinny_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer)
    img_hash = db.Column(db.String(40), index=True, unique=True, primary_key=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_skinny_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))  # new
    color_cats = db.Column(ARRAY(db.String))  # new
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))  # new
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String), index=True)
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_2 = db.Column(ARRAY(db.Integer))
    color_3 = db.Column(ARRAY(db.Integer))
    color_4 = db.Column(ARRAY(db.Integer))
    color_5 = db.Column(ARRAY(db.Integer))
    color_6 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 color_1,
                 color_2,
                 color_3,
                 color_4,
                 color_5,
                 color_6,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5
        self.color_6 = color_6
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesFullWomenB(db.Model):
    __tablename__ = 'images_full_women_b'

    __table_args__ = (
        db.Index('images_full_women_b_name_idx', 'img_full_name', postgresql_ops={'img_full_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), db.ForeignKey("images_skinny_women_b.img_hash"), index=True, unique=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_full_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String), index=True)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    color_3 = db.Column(ARRAY(db.Integer))
    color_3_hex = db.Column(db.String)
    color_4 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_4_hex = db.Column(db.String)
    color_5 = db.Column(ARRAY(db.Integer))
    color_5_hex = db.Column(db.String)
    color_6 = db.Column(ARRAY(db.Integer))
    color_6_hex = db.Column(db.String)
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    encoding_vgg16 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 color_1,
                 color_1_hex,
                 color_2,
                 color_2_hex,
                 color_3,
                 color_3_hex,
                 color_4,
                 color_4_hex,
                 color_5,
                 color_5_hex,
                 color_6,
                 color_6_hex,
                 size_stock,
                 in_stock,
                 encoding_vgg16,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.color_3 = color_3
        self.color_3_hex = color_3_hex
        self.color_4 = color_4
        self.color_4_hex = color_4_hex
        self.color_5 = color_5
        self.color_5_hex = color_5_hex
        self.color_6 = color_6
        self.color_6_hex = color_6_hex
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.encoding_vgg16 = encoding_vgg16
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesFullWomenC(db.Model):
    __tablename__ = 'images_full_women_c'

    __table_args__ = (
        db.Index('images_full_women_c_name_idx', 'img_full_name', postgresql_ops={'img_full_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), db.ForeignKey("images_skinny_women_c.img_hash"), index=True, unique=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_full_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String), index=True)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    color_3 = db.Column(ARRAY(db.Integer))
    color_3_hex = db.Column(db.String)
    color_4 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_4_hex = db.Column(db.String)
    color_5 = db.Column(ARRAY(db.Integer))
    color_5_hex = db.Column(db.String)
    color_6 = db.Column(ARRAY(db.Integer))
    color_6_hex = db.Column(db.String)
    color_hist = db.Column(ARRAY(db.Integer))
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    encoding_vgg16 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 color_1,
                 color_1_hex,
                 color_2,
                 color_2_hex,
                 color_3,
                 color_3_hex,
                 color_4,
                 color_4_hex,
                 color_5,
                 color_5_hex,
                 color_6,
                 color_6_hex,
                 color_hist,
                 size_stock,
                 in_stock,
                 encoding_vgg16,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.color_3 = color_3
        self.color_3_hex = color_3_hex
        self.color_4 = color_4
        self.color_4_hex = color_4_hex
        self.color_5 = color_5
        self.color_5_hex = color_5_hex
        self.color_6 = color_6
        self.color_6_hex = color_6_hex
        self.color_hist = color_hist
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.encoding_vgg16 = encoding_vgg16
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesFullMenB(db.Model):
    __tablename__ = 'images_full_men_b'

    __table_args__ = (
        db.Index('images_full_men_b_name_idx', 'img_full_name', postgresql_ops={'img_full_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), db.ForeignKey("images_skinny_men_b.img_hash"), index=True, unique=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_full_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String), index=True)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    color_3 = db.Column(ARRAY(db.Integer))
    color_3_hex = db.Column(db.String)
    color_4 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_4_hex = db.Column(db.String)
    color_5 = db.Column(ARRAY(db.Integer))
    color_5_hex = db.Column(db.String)
    color_6 = db.Column(ARRAY(db.Integer))
    color_6_hex = db.Column(db.String)
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    encoding_vgg16 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 color_1,
                 color_1_hex,
                 color_2,
                 color_2_hex,
                 color_3,
                 color_3_hex,
                 color_4,
                 color_4_hex,
                 color_5,
                 color_5_hex,
                 color_6,
                 color_6_hex,
                 size_stock,
                 in_stock,
                 encoding_vgg16,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.color_3 = color_3
        self.color_3_hex = color_3_hex
        self.color_4 = color_4
        self.color_4_hex = color_4_hex
        self.color_5 = color_5
        self.color_5_hex = color_5_hex
        self.color_6 = color_6
        self.color_6_hex = color_6_hex
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.encoding_vgg16 = encoding_vgg16
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ImagesFullMenC(db.Model):
    __tablename__ = 'images_full_men_c'

    __table_args__ = (
        db.Index('images_full_men_c_name_idx', 'img_full_name', postgresql_ops={'img_full_name': "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    id = db.Column(db.Integer, primary_key=True)
    img_hash = db.Column(db.String(40), db.ForeignKey("images_skinny_men_c.img_hash"), index=True, unique=True)
    img_url = db.Column(db.String)
    prod_id = db.Column(db.String)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    color_string = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    name = db.Column('img_full_name', db.Text, index=True)
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.String)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String), index=True)
    color_1 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = db.Column(db.String)
    color_2 = db.Column(ARRAY(db.Integer))
    color_2_hex = db.Column(db.String)
    color_3 = db.Column(ARRAY(db.Integer))
    color_3_hex = db.Column(db.String)
    color_4 = db.Column(ARRAY(db.Integer))  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_4_hex = db.Column(db.String)
    color_5 = db.Column(ARRAY(db.Integer))
    color_5_hex = db.Column(db.String)
    color_6 = db.Column(ARRAY(db.Integer))
    color_6_hex = db.Column(db.String)
    color_hist = db.Column(ARRAY(db.Integer))
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    encoding_vgg16 = db.Column(ARRAY(db.Integer))
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 img_hash,
                 img_url,
                 prod_id,
                 prod_url,
                 brand,
                 color_string,
                 date,
                 date_updated,
                 name,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 color_1,
                 color_1_hex,
                 color_2,
                 color_2_hex,
                 color_3,
                 color_3_hex,
                 color_4,
                 color_4_hex,
                 color_5,
                 color_5_hex,
                 color_6,
                 color_6_hex,
                 color_hist,
                 size_stock,
                 in_stock,
                 encoding_vgg16,
                 is_deleted):

        self.img_hash = img_hash
        self.img_url = img_url
        self.prod_id = prod_id
        self.prod_url = prod_url
        self.brand = brand
        self.color_string = color_string
        self.date = date
        self.date_updated = date_updated
        self.name = name
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.color_1 = color_1
        self.color_1_hex = color_1_hex
        self.color_2 = color_2
        self.color_2_hex = color_2_hex
        self.color_3 = color_3
        self.color_3_hex = color_3_hex
        self.color_4 = color_4
        self.color_4_hex = color_4_hex
        self.color_5 = color_5
        self.color_5_hex = color_5_hex
        self.color_6 = color_6
        self.color_6_hex = color_6_hex
        self.color_hist = color_hist
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.encoding_vgg16 = encoding_vgg16
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ProductsWomenB(db.Model):
    __tablename__ = 'prods_women_b'
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.String(40), index=True, unique=True)
    name = db.Column(db.Text, index=True)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    category = db.Column(db.Text)
    color_string = db.Column(db.Text)
    currency = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_hash = db.Column(ARRAY(db.String), index=True)
    image_urls = db.Column(ARRAY(db.String))
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.Text)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String))
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    is_fav = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 prod_id,
                 name,
                 prod_url,
                 brand,
                 category,
                 color_string,
                 currency,
                 date,
                 date_updated,
                 description,
                 image_hash,
                 image_urls,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 is_fav,
                 is_deleted):
        self.prod_id = prod_id
        self.name = name
        self.prod_url = prod_url
        self.brand = brand
        self.category = category
        self.color_string = color_string
        self.currency = currency
        self.date = date
        self.date_updated = date_updated
        self.description = description
        self.image_hash = image_hash
        self.image_urls = image_urls
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.is_fav = is_fav
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ProductsWomenC(db.Model):
    __tablename__ = 'prods_women_c'
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.String(40), index=True, unique=True)
    name = db.Column(db.Text, index=True)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    category = db.Column(db.Text)
    color_string = db.Column(db.Text)
    currency = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_hash = db.Column(ARRAY(db.String), index=True)
    image_urls = db.Column(ARRAY(db.String))
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.Text)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String))
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    is_fav = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)
    is_old = db.Column(db.Boolean)

    def __init__(self,
                 prod_id,
                 name,
                 prod_url,
                 brand,
                 category,
                 color_string,
                 currency,
                 date,
                 date_updated,
                 description,
                 image_hash,
                 image_urls,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 is_fav,
                 is_deleted,
                 is_old):
        self.prod_id = prod_id
        self.name = name
        self.prod_url = prod_url
        self.brand = brand
        self.category = category
        self.color_string = color_string
        self.currency = currency
        self.date = date
        self.date_updated = date_updated
        self.description = description
        self.image_hash = image_hash
        self.image_urls = image_urls
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.is_fav = is_fav
        self.is_deleted = is_deleted
        self.is_old = is_old

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ProductsMenB(db.Model):
    __tablename__ = 'prods_men_b'
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.String(40), index=True, unique=True)
    name = db.Column(db.Text, index=True)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    category = db.Column(db.Text)
    color_string = db.Column(db.Text)
    currency = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_hash = db.Column(ARRAY(db.String), index=True)
    image_urls = db.Column(ARRAY(db.String))
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.Text)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String))
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    is_fav = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)

    def __init__(self,
                 prod_id,
                 name,
                 prod_url,
                 brand,
                 category,
                 color_string,
                 currency,
                 date,
                 date_updated,
                 description,
                 image_hash,
                 image_urls,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 is_fav,
                 is_deleted):
        self.prod_id = prod_id
        self.name = name
        self.prod_url = prod_url
        self.brand = brand
        self.category = category
        self.color_string = color_string
        self.currency = currency
        self.date = date
        self.date_updated = date_updated
        self.description = description
        self.image_hash = image_hash
        self.image_urls = image_urls
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.is_fav = is_fav
        self.is_deleted = is_deleted

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class ProductsMenC(db.Model):
    __tablename__ = 'prods_men_c'
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.String(40), index=True, unique=True)
    name = db.Column(db.Text, index=True)
    prod_url = db.Column(db.String)
    brand = db.Column(db.Text)
    category = db.Column(db.Text)
    color_string = db.Column(db.Text)
    currency = db.Column(db.String)
    date = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_hash = db.Column(ARRAY(db.String), index=True)
    image_urls = db.Column(ARRAY(db.String))
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    saleprice = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    sex = db.Column(db.String)
    shop = db.Column(db.Text)
    kind_cats = db.Column(ARRAY(db.String), index=True)
    pattern_cats = db.Column(ARRAY(db.String))
    color_cats = db.Column(ARRAY(db.String))
    style_cats = db.Column(ARRAY(db.String))
    material_cats = db.Column(ARRAY(db.String))
    attribute_cats = db.Column(ARRAY(db.String))
    length_cats = db.Column(ARRAY(db.String))
    filter_cats = db.Column(ARRAY(db.String))
    all_cats = db.Column(ARRAY(db.String))
    size_stock = db.Column(MutableList.as_mutable(JSONB))
    in_stock = db.Column(db.Boolean)
    is_fav = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)
    is_old = db.Column(db.Boolean)

    def __init__(self,
                 prod_id,
                 name,
                 prod_url,
                 brand,
                 category,
                 color_string,
                 currency,
                 date,
                 date_updated,
                 description,
                 image_hash,
                 image_urls,
                 price,
                 sale,
                 saleprice,
                 discount_rate,
                 sex,
                 shop,
                 kind_cats,
                 pattern_cats,
                 color_cats,
                 style_cats,
                 material_cats,
                 attribute_cats,
                 length_cats,
                 filter_cats,
                 all_cats,
                 size_stock,
                 in_stock,
                 is_fav,
                 is_deleted,
                 is_old):
        self.prod_id = prod_id
        self.name = name
        self.prod_url = prod_url
        self.brand = brand
        self.category = category
        self.color_string = color_string
        self.currency = currency
        self.date = date
        self.date_updated = date_updated
        self.description = description
        self.image_hash = image_hash
        self.image_urls = image_urls
        self.price = price
        self.sale = sale
        self.saleprice = saleprice
        self.discount_rate = discount_rate
        self.sex = sex
        self.shop = shop
        self.kind_cats = kind_cats
        self.pattern_cats = pattern_cats
        self.color_cats = color_cats
        self.style_cats = style_cats
        self.material_cats = material_cats
        self.attribute_cats = attribute_cats
        self.length_cats = length_cats
        self.filter_cats = filter_cats
        self.all_cats = all_cats
        self.size_stock = size_stock
        self.in_stock = in_stock
        self.is_fav = is_fav
        self.is_deleted = is_deleted
        self.is_old = is_old

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_name(self):
        return self.name


class LoadingContent(db.Model):
    __tablename__ = 'loading_content'
    id = db.Column(db.Integer, primary_key=True)
    content_date = db.Column(db.Integer)
    content_type = db.Column(db.String)
    content_text = db.Column(db.String)
    content_image = db.Column(db.String)

    def __init__(
            self,
            content_date,
            content_type,
            content_text,
            content_image):
        self.content_date = content_date
        self.content_type = content_type
        self.content_text = content_text
        self.content_image = content_image

    def __repr__(self):
        return '<id={}>'.format(self.id)

    def return_date(self):
        return self.content_date
