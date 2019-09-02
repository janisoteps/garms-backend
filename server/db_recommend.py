from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ProductsSchema, ImageSchema
# import scipy.spatial as spatial
# import numpy as np
# from operator import itemgetter
import json
# from color_text import color_check
# from flask import jsonify
from cats import Cats


def recommend_similar_tags(db, User, Products, data):
    req_email = data['email']
    req_sex = data['sex']
    user_data = User.query.filter_by(email=req_email).first()
    if user_data is None:
        return 'Invalid user email'
    user_wardrobe = user_data.wardrobe
    user_looks = user_data.looks
    suggestions = []

    for look in user_looks:
        outfits = [outfit['prod_id'] for outfit in user_wardrobe if outfit['look_name'] == look['look_name']]
        # print('outfits')
        # print(outfits)
        if len(outfits) > 0:
            query_prods = db.session.query(Products).filter(Products.prod_hash.in_(outfits)).all()
            look_cats_kind = []
            look_cats_all = []
            for query_prod in query_prods:
                query_name = query_prod.name
                # print(f'query_name={query_name}')
                for query_word in query_name.split(' '):
                    # print(f'query_word={query_word}')
                    if query_word.lower() in Cats().kind_cats and query_word.lower() not in look_cats_kind:
                        # print(f'added to look_cats_kind: {query_word.lower()}')
                        look_cats_kind.append(query_word.lower())
                    if query_word.lower() in Cats().all_cats and query_word.lower() not in look_cats_all:
                        # print(f'added to look_cats_all: {query_word.lower()}')
                        look_cats_all.append(query_word.lower())

            # print('look cats kind')
            # print(look_cats_kind)
            # print('look cats all')
            # print(look_cats_all)

            kind_conditions = []
            all_conditions = []

            for tag in look_cats_kind:
                kind_conditions.append(
                    func.lower(Products.name).ilike('%{}%'.format(tag)) | Products.img_cats_sc_txt.any(tag)
                )
            for all_tag in look_cats_all:
                all_conditions.append(
                    func.lower(Products.name).ilike('%{}%'.format(all_tag)) | Products.img_cats_sc_txt.any(all_tag)
                )

            # print('KIND CONDS')
            # print(kind_conditions)
            # print('ALL CONDS')
            # print(all_conditions)

            query = db.session.query(Products).filter(
                and_(
                    and_(or_(*kind_conditions), (Products.sex == req_sex)),
                    or_(or_(*kind_conditions), or_(*all_conditions))
                )
            )
            query_results = query.order_by(func.random()).limit(10).all()
            prod_results = []
            for query_result in query_results:
                prod_serial = ProductsSchema().dump(query_result)
                prod_results.append(prod_serial)

            suggestions.append({
                'look_name': look['look_name'],
                'prod_suggestions': prod_results
            })

    return json.dumps(suggestions)
