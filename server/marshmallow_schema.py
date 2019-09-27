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


class SizeStockSchema(Schema):
    stock = fields.String()
    size = fields.String()


class ProductSchemaV2(Schema):
    id = fields.Integer()
    prod_id = fields.String()
    name = fields.String()
    prod_url = fields.String()
    brand = fields.String()
    category = fields.String()
    color_string = fields.String()
    currency = fields.String()
    date = fields.String()
    description = fields.String()
    image_hash = fields.List(fields.String())
    image_urls = fields.List(fields.String())
    price = fields.Number()
    sale = fields.Boolean()
    saleprice = fields.Number()
    sex = fields.String()
    shop = fields.String()
    size_stock = fields.List(fields.Nested(SizeStockSchema))
    kind_cats = fields.List(fields.String())
    color_pattern_cats = fields.List(fields.String())
    style_cats = fields.List(fields.String())
    material_cats = fields.List(fields.String())
    attribute_cats = fields.List(fields.String())
    filter_cats = fields.List(fields.String())
    all_cats = fields.List(fields.String())
    kind_arr = fields.List(fields.Integer())
    col_pat_arr = fields.List(fields.Integer())
    style_arr = fields.List(fields.Integer())
    material_arr = fields.List(fields.Integer())
    attr_arr = fields.List(fields.Integer())
    filter_arr = fields.List(fields.Integer())
    all_arr = fields.List(fields.Integer())


class ImageSchemaV2(Schema):
    id = fields.Integer()
    img_hash = fields.String()
    img_url = fields.String()
    prod_id = fields.String()
    prod_url = fields.String()
    color_string = fields.String()
    date = fields.Integer()
    name = fields.String()
    price = fields.Number()
    sale = fields.Boolean()
    saleprice = fields.Number()
    sex = fields.String()
    shop = fields.String()
    kind_cats = fields.List(fields.String())
    color_pattern_cats = fields.List(fields.String())
    style_cats = fields.List(fields.String())
    material_cats = fields.List(fields.String())
    attribute_cats = fields.List(fields.String())
    filter_cats = fields.List(fields.String())
    all_cats = fields.List(fields.String())
    kind_arr = fields.List(fields.Integer())
    col_pat_arr = fields.List(fields.Integer())
    style_arr = fields.List(fields.Integer())
    material_arr = fields.List(fields.Integer())
    attr_arr = fields.List(fields.Integer())
    filter_arr = fields.List(fields.Integer())
    all_arr = fields.List(fields.Integer())
    color_1 = fields.List(fields.Integer())  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = fields.String()
    color_2 = fields.List(fields.Integer())
    color_2_hex = fields.String()
    color_3 = fields.List(fields.Integer())
    color_3_hex = fields.String()
    encoding_crop = fields.List(fields.Integer())
    size_stock = fields.List(fields.Nested(SizeStockSchema))
    in_stock = fields.Boolean()


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
