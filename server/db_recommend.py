from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ProductsSchema, ImageSchema, ProductSchemaV2
import json
import data.cats as cats


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
            outfits = [outfit['prod_id'] for outfit in user_wardrobe if outfit['look_name'] == look['look_name']]
            # print('outfits')
            # print(outfits)
            if len(outfits) > 0:
                # print('getting user outfits')
                query_prods = db.session.query(ProductsV2).filter(ProductsV2.prod_id.in_(outfits)).all()
                # print('loaded user outfits')
                look_cats_kind = []
                look_cats_all = []
                for query_prod in query_prods:
                    query_name = query_prod.name
                    # print(f'query_name={query_name}')
                    for query_word in query_name.split(' '):
                        # print(f'query_word={query_word}')
                        if query_word.lower() in cats.Cats().kind_cats and query_word.lower() not in look_cats_kind:
                            # print(f'added to look_cats_kind: {query_word.lower()}')
                            look_cats_kind.append(query_word.lower())
                        if query_word.lower() in cats.Cats().all_cats and query_word.lower() not in look_cats_all:
                            # print(f'added to look_cats_all: {query_word.lower()}')
                            look_cats_all.append(query_word.lower())

                for tag in look_cats_kind:
                    kind_conditions.append(
                        ProductsV2.kind_cats.any(tag)
                    )

        print('querying for recommended prods')
        query = db.session.query(ProductsV2).filter(
            and_(or_(*kind_conditions), (ProductsV2.sex == req_sex), ProductsV2.prod_id.isnot(None))
        )

        query_results = query.order_by(func.random()).limit(30).all()
        print('loaded recommended prods')
        prod_results = []
        for query_result in query_results:
            prod_serial = ProductSchemaV2().dump(query_result)
            prod_results.append(prod_serial)

        suggestions.append({
            'look_name': look['look_name'],
            'prod_suggestions': prod_results
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
