from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ProductsSchema, ImageSchema, ProductSchemaV2
import json
import data.cats as cats
from random import shuffle


def recommend_similar_tags(db, User, ProductsV2, data):
    req_email = data['email']
    req_sex = data['sex']
    user_data = User.query.filter_by(email=req_email).first()
    if user_data is None:
        return 'Invalid user email'
    user_wardrobe = user_data.wardrobe
    user_looks = user_data.looks
    suggestions = []

    if user_looks is not None and user_wardrobe is not None:
        kind_conditions = []

        for look in user_looks:
            print(look)
            outfits = [outfit['prod_id'] for outfit in user_wardrobe if outfit['look_name'] == look['look_name']]
            if len(outfits) > 0:
                query_prods = db.session.query(ProductsV2).filter(ProductsV2.prod_id.in_(outfits)).all()
                look_cats_kind = []
                for query_prod in query_prods:
                    print(query_prod.name)
                    query_kind_cats = query_prod.kind_cats
                    for query_kind_cat in query_kind_cats:
                        if query_kind_cat not in look_cats_kind:
                            look_cats_kind.append(query_kind_cat)

                print(look_cats_kind)
                for cat in look_cats_kind:
                    kind_conditions.append(
                        (ProductsV2.kind_cats.any(cat))
                    )

            print('querying for recommended prods')
            query = db.session.query(ProductsV2).filter(
                and_(or_(*kind_conditions), (ProductsV2.sex == req_sex), ProductsV2.prod_id.isnot(None))
            )

            query_results = query.order_by(func.random()).limit(10).all()
            print('loaded recommended prods')
            # prod_results = []
            for query_result in query_results:
                prod_serial = ProductSchemaV2().dump(query_result)
                # prod_results.append(prod_serial)

                suggestions.append({
                    'look_name': look['look_name'],
                    'prod_suggestions': [prod_serial]
                })

    else:
        query = db.session.query(ProductsV2).filter(ProductsV2.prod_id.isnot(None)).filter(ProductsV2.sex == req_sex)
        query_results = query.order_by(func.random()).limit(30).all()
        prod_results = []
        for query_result in query_results:
            prod_serial = ProductSchemaV2().dump(query_result)
            prod_results.append(prod_serial)
        suggestions.append({
            'look_name': 'All',
            'prod_suggestions': prod_results
        })

    shuffle(suggestions)
    return json.dumps(suggestions)


def recommend_from_random(db, ProductsV2, data):
    req_sex = data['sex']
    print(f'req_sex = {req_sex}')
    if req_sex is not '':
        if req_sex == 'both':
            query = db.session.query(ProductsV2).filter(ProductsV2.prod_id.isnot(None))
        else:
            query = db.session.query(ProductsV2).filter(ProductsV2.sex == req_sex).filter(ProductsV2.prod_id.isnot(None))
    else:
        query = db.session.query(ProductsV2).filter(ProductsV2.prod_id.isnot(None))

    query_results = query.order_by(func.random()).limit(30).all()
    prod_results = []
    for query_result in query_results:
        prod_serial = ProductSchemaV2().dump(query_result)
        prod_results.append(prod_serial)

    suggestions = [
        {
            'look_name': None,
            'prod_suggestions': prod_results
        }
    ]

    return json.dumps(suggestions)
