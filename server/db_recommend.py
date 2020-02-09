from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ProductSchemaV2, ProductsWomenASchema
import json
import data.cats as cats
from random import shuffle
from operator import add
import random


def recommend_similar_tags(db, User, Products, data):
    req_email = data['email']
    req_sex = data['sex']
    req_look_name = data['req_looks']
    user_data = User.query.filter_by(email=req_email).first()
    if user_data is None:
        return 'Invalid user email'
    user_wardrobe = user_data.wardrobe
    user_looks = user_data.looks
    suggestions = []

    if user_looks is not None and user_wardrobe is not None:
        outfits = []
        if req_look_name is None:
            for look in user_looks:
                print(look)
                outfits += [outfit['prod_id'] for outfit in user_wardrobe if outfit['look_name'] == look['look_name']]

        else:
            for look in user_looks:
                print(look)
                outfits += [outfit['prod_id'] for outfit in user_wardrobe if outfit['look_name'] == req_look_name]

        if len(outfits) > 0:
            kind_conditions = []
            query_prods = db.session.query(Products).filter(Products.prod_id.in_(outfits)).all()

            print(f'len query_prods: {len(query_prods)}')
            look_cats_kind = []
            kind_cat_counts = []
            for query_prod in query_prods:
                # print(query_prod.name)
                query_kind_cats = query_prod.kind_cats
                for query_kind_cat in query_kind_cats:
                    if query_kind_cat not in look_cats_kind:
                        look_cats_kind.append(query_kind_cat)
                        kind_cat_counts.append((query_kind_cat, 1))
                    else:
                        kind_cat_index = look_cats_kind.index(query_kind_cat)
                        kind_cat_counts[kind_cat_index] = (kind_cat_counts[kind_cat_index][0], kind_cat_counts[kind_cat_index][1] + 1)

            sorted_kind_cats = sorted(kind_cat_counts, key=lambda tup: tup[1], reverse=True)
            top_cats = sorted_kind_cats[:10]
            if len(top_cats) > 10:
                top_cats_rand = random.sample(top_cats, 5)
            else:
                top_cats_rand = random.sample(top_cats, int(len(top_cats) / 2))
            print(f'top cats: {top_cats_rand}')

            for top_cat in top_cats_rand:
                # kind_conditions.append(
                #     func.lower(ProductsV2.name).ilike('%{}%'.format(top_cat[0]))
                # )
                kind_conditions.append(
                    (Products.kind_cats.any(top_cat[0]))
                )

            print('querying for recommended prods')
            # query = db.session.query(Products).filter(
            #     and_(
            #         or_(*kind_conditions),
            #         (Products.sex == req_sex),
            #         Products.prod_id.isnot(None),
            #         (Products.shop != "Farfetch")
            #     )
            # )
            query = db.session.query(Products).filter(
                and_(
                    or_(*kind_conditions),
                    (Products.sex == req_sex),
                    Products.prod_id.isnot(None)
                )
            )

            query_results = query.order_by(func.random()).limit(40).all()
            print(f'loaded recommended prods, LENGTH: {len(query_results)}')
            # prod_results = []
            for query_result in query_results:
                if len(query_result.image_urls) > 0:
                    prod_serial = ProductsWomenASchema().dump(query_result)

                    suggestions.append({
                        'look_name': 'all' if req_look_name is None else req_look_name,
                        'prod_suggestions': [prod_serial]
                    })
            print('---------------------------')

    else:
        query = db.session.query(Products).filter(Products.prod_id.isnot(None)).filter(and_(
            Products.sex == req_sex,
            (Products.shop != "Farfetch")
        ))
        query_results = query.order_by(func.random()).limit(40).all()
        prod_results = []
        for query_result in query_results:
            if len(query_result.image_urls) > 0:
                if req_sex == 'women':
                    prod_serial = ProductsWomenASchema().dump(query_result)
                else:
                    prod_serial = ProductSchemaV2().dump(query_result)
                prod_results.append(prod_serial)
        suggestions.append({
            'look_name': 'All',
            'prod_suggestions': prod_results
        })

    shuffle(suggestions)
    return json.dumps(suggestions)


def recommend_from_random(db, Products, data):
    req_sex = data['sex']
    print(f'req_sex = {req_sex}')
    if req_sex is not '':
        if req_sex == 'both':
            query = db.session.query(Products).filter(Products.prod_id.isnot(None))
        else:
            query = db.session.query(Products).filter(Products.sex == req_sex).filter(Products.prod_id.isnot(None))
    else:
        query = db.session.query(Products).filter(Products.prod_id.isnot(None))

    query_results = query.filter(Products.shop != "Farfetch").order_by(func.random()).limit(40).all()
    prod_results = []
    for query_result in query_results:
        if len(query_result.image_urls) > 0:
            if req_sex == 'women':
                prod_serial = ProductsWomenASchema().dump(query_result)
            else:
                prod_serial = ProductSchemaV2().dump(query_result)
            prod_results.append(prod_serial)

    suggestions = [
        {
            'look_name': None,
            'prod_suggestions': prod_results
        }
    ]

    return json.dumps(suggestions)
