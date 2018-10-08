from marshmallow import Schema, fields


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


class InstaMentionSchema(Schema):
    id = fields.Integer()
    mention_username = fields.String()
    comment_id = fields.String()
    mention_timestamp = fields.String()
    media_id = fields.String()
    media_type = fields.String()
    media_url = fields.String()
    media_permalink = fields.String()
    owner_username = fields.String()
