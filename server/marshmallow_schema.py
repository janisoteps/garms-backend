from marshmallow import Schema, fields


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
    is_fav = fields.Boolean()


class ImageSchemaV2(Schema):
    id = fields.Integer()
    img_hash = fields.String()
    img_url = fields.String()
    prod_id = fields.String()
    prod_url = fields.String()
    brand = fields.String()
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
    encoding_vgg16 = fields.List(fields.Integer())


class ImagesFullWomenASchema(Schema):
    id = fields.Integer()
    img_hash = fields.String()
    img_url = fields.String()
    prod_id = fields.String()
    prod_url = fields.String()
    brand = fields.String()
    color_string = fields.String()
    date = fields.Integer()
    name = fields.String()
    price = fields.Number()
    sale = fields.Boolean()
    saleprice = fields.Number()
    discount_rate = fields.Number()
    sex = fields.String()
    shop = fields.String()
    kind_cats = fields.List(fields.String())
    pattern_cats = fields.List(fields.String())
    color_cats = fields.List(fields.String())
    style_cats = fields.List(fields.String())
    material_cats = fields.List(fields.String())
    attribute_cats = fields.List(fields.String())
    length_cats = fields.List(fields.String())
    filter_cats = fields.List(fields.String())
    all_cats = fields.List(fields.String())
    color_1 = fields.List(fields.Integer())  # Array of 3 integers from 0 to 255 representing 1 RGB value
    color_1_hex = fields.String()
    color_2 = fields.List(fields.Integer())
    color_2_hex = fields.String()
    color_3 = fields.List(fields.Integer())
    color_3_hex = fields.String()
    size_stock = fields.List(fields.Nested(SizeStockSchema))
    in_stock = fields.Boolean()
    encoding_vgg16 = fields.List(fields.Integer())


class ProductsWomenASchema(Schema):
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
    discount_rate = fields.Number()
    sex = fields.String()
    shop = fields.String()
    kind_cats = fields.List(fields.String())
    pattern_cats = fields.List(fields.String())
    color_cats = fields.List(fields.String())
    style_cats = fields.List(fields.String())
    material_cats = fields.List(fields.String())
    attribute_cats = fields.List(fields.String())
    length_cats = fields.List(fields.String())
    filter_cats = fields.List(fields.String())
    all_cats = fields.List(fields.String())
    size_stock = fields.List(fields.Nested(SizeStockSchema))
    in_stock = fields.Boolean()
    is_fav = fields.Boolean()


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


class LoadingContentSchema(Schema):
    id = fields.Integer()
    content_date = fields.Integer()
    content_type = fields.String()
    content_text = fields.String()
    content_image = fields.String()
