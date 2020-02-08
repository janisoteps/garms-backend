from sqlalchemy import func, and_, or_
from marshmallow_schema import ProductsWomenASchema
import json


def get_deals(db, ImagesSkinny, Products, data):
    req_sex = data['sex']
    req_cats = data['cats']
    req_shops = data['shops']
    req_brands = data['brands']

    sex_conditions = []
    cat_conditions = []
    shop_conditions = []
    brand_conditions = []

    sex_conditions.append(
        (ImagesSkinny.sex == req_sex)
    )
    for req_cat in req_cats:
        cat_conditions.append(
            (ImagesSkinny.all_cats.any(req_cat))
        )
    for req_shop in req_shops:
        shop_conditions.append(
            (func.lower(ImagesSkinny.shop).op('%%')(req_shop.lower()))
        )
    for req_brand in req_brands:
        brand_conditions.append(
            (func.lower(ImagesSkinny.brand).op('%%')(req_brand.lower()))
        )

    query = db.session.query(ImagesSkinny).filter(
        and_(
            and_(*sex_conditions),
            and_(*cat_conditions),
            or_(*shop_conditions),
            or_(*brand_conditions)
        )
    )
    query_results = query.order_by(ImagesSkinny.discount_rate.desc()).limit(100).all()

    prod_results = []
    prod_check = set()
    print('Obtaining result data')
    for query_result in query_results:
        result_prod_id = query_result.prod_id

        if result_prod_id not in prod_check:
            prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
            prod_serial = ProductsWomenASchema().dump(prod_search)
            prod_check.add(result_prod_id)
            prod_results.append(prod_serial[0])

    suggestions = {
        'prod_suggestions': prod_results
    }

    return json.dumps(suggestions)
