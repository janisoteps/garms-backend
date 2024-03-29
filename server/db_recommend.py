from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ProductsSchema, ImagesSkinnySchema
import json
from random import shuffle
import random


def recommend_similar_tags(db, User, Products, data):
    try:
        req_email = data['email']
    except:
        req_email = None
    req_sex = data['sex']
    req_look_name = data['req_looks']
    try:
        prev_prod_ids = data['prev_prod_ids']
    except:
        prev_prod_ids = None

    if req_email is not None:
        user_data = User.query.filter_by(email=req_email).first()
        if user_data is None:
            return 'Invalid user email'
        user_wardrobe = user_data.wardrobe
        user_looks = user_data.looks
        suggestions = []
        base_conds = []

        if prev_prod_ids is not None:
            for prev_prod_id in prev_prod_ids:
                base_conds.append(
                    Products.prod_id != prev_prod_id
                )

        if user_looks is not None and user_wardrobe is not None:
            outfits = []
            if req_look_name is None:
                for look in user_looks:
                    outfits += [outfit['prod_id'] for outfit in user_wardrobe if outfit['look_name'] == look['look_name']]

            else:
                for look in user_looks:
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
                print(f'sorted cats: {sorted_kind_cats}')
                top_cats = sorted_kind_cats[:int(len(sorted_kind_cats) / 2)]
                print(f'half cats: {top_cats}')
                if len(top_cats) > 10:
                    top_cats_rand = random.sample(top_cats, 5)
                else:
                    top_cats_rand = top_cats
                print(f'picked cats: {top_cats_rand}')

                for top_cat in top_cats_rand:
                    kind_conditions.append(
                        (Products.kind_cats.any(top_cat[0]))
                    )

                print('querying for recommended prods')

                query = db.session.query(Products).filter(
                    and_(
                        or_(*kind_conditions),
                        and_(*base_conds),
                        (Products.sex == req_sex),
                        Products.prod_id.isnot(None),
                        Products.is_deleted.isnot(True),
                        Products.is_old.isnot(True),
                        Products.price > 40,
                        Products.price < 100
                    )
                )

                query_results = query.order_by(func.random()).limit(40).all()
                print(f'loaded recommended prods, LENGTH: {len(query_results)}')
                # prod_results = []
                for query_result in query_results:
                    if len(query_result.image_urls) > 0:
                        prod_serial = ProductsSchema().dump(query_result)

                        suggestions.append({
                            'look_name': 'all' if req_look_name is None else req_look_name,
                            'prod_suggestions': [prod_serial]
                        })
                print('---------------------------')

        else:
            query = db.session.query(Products).filter(Products.prod_id.isnot(None)).filter(and_(
                Products.sex == req_sex,
                and_(*base_conds),
                (Products.shop != "Farfetch")
            ))
            query_results = query.order_by(func.random()).limit(40).all()
            prod_results = []
            for query_result in query_results:
                if len(query_result.image_urls) > 0:
                    prod_serial = ProductsSchema().dump(query_result)
                    prod_results.append(prod_serial)
            suggestions.append({
                'look_name': 'All',
                'prod_suggestions': prod_results
            })

        shuffle(suggestions)
        return json.dumps(suggestions)

    else:
        print('Recommending random: invalid email')
        rand_conds = []
        rand_conds.append(
            and_(
                (Products.price > 40),
                (Products.price < 100)
            )
        )
        rand_conds.append(
            (Products.prod_id.isnot(None))
        )
        rand_conds.append(
            Products.is_deleted.isnot(True)
        )
        rand_conds.append(
            Products.is_old.isnot(True)
        )
        if prev_prod_ids is not None:
            for prev_prod_id in prev_prod_ids:
                rand_conds.append(
                    Products.prod_id != prev_prod_id
                )

        query = db.session.query(Products).filter(
            and_(*rand_conds)
        )
        query_results = query.order_by(func.random()).limit(40).all()
        prod_results = []
        for query_result in query_results:
            if len(query_result.image_urls) > 0:
                prod_serial = ProductsSchema().dump(query_result)
                prod_results.append(prod_serial)

        suggestions = [
            {
                'look_name': None,
                'prod_suggestions': prod_results
            }
        ]

        return json.dumps(suggestions)


def recommend_from_onboarding_faves(db, Products, data):
    req_sex = data['sex']
    req_fave_outfits = data['fave_outfits']
    try:
        prev_prod_ids = data['prev_prod_ids']
    except:
        prev_prod_ids = None
    recommend_conds = []
    kind_conds = []

    req_kind_cats = []
    kind_cat_counts = []
    for req_fave_outfit in req_fave_outfits:
        fave_kind_cats = req_fave_outfit['kind_cats']
        for fave_kind_cat in fave_kind_cats:
            if fave_kind_cat not in req_kind_cats:
                req_kind_cats.append(fave_kind_cat)
                kind_cat_counts.append((fave_kind_cat, 1))
            else:
                kind_cat_index = req_kind_cats.index(fave_kind_cat)
                kind_cat_counts[kind_cat_index] = (kind_cat_counts[kind_cat_index][0], kind_cat_counts[kind_cat_index][1] + 1)
    sorted_kind_cats = sorted(kind_cat_counts, key=lambda tup: tup[1], reverse=True)
    top_kind_cats = sorted_kind_cats[:10]
    if len(top_kind_cats) > 10:
        top_cats_rand = random.sample(top_kind_cats, 5)
    else:
        top_cats_rand = top_kind_cats
    print(f'top cats: {top_cats_rand}')

    for top_cat in top_cats_rand:
        kind_conds.append(
            (Products.name.ilike('%{}%'.format(top_cat[0])))
        )
    recommend_conds.append(
        and_(
            (Products.price > 40),
            (Products.price < 100)
        )
    )
    recommend_conds.append(
        (Products.prod_id.isnot(None))
    )
    recommend_conds.append(
        (Products.is_old.isnot(True))
    )
    recommend_conds.append(
        Products.is_deleted.isnot(True)
    )
    if prev_prod_ids is not None:
        for prev_prod_id in prev_prod_ids:
            recommend_conds.append(
                Products.prod_id != prev_prod_id
            )

    query = db.session.query(Products).filter(
        and_(
            and_(*recommend_conds),
            or_(*kind_conds)
        )
    )
    query_results = query.order_by(func.random()).limit(40).all()

    prod_results = []
    for query_result in query_results:
        if len(query_result.image_urls) > 0:
            prod_serial = ProductsSchema().dump(query_result)
            prod_results.append(prod_serial)

    suggestions = [
        {
            'look_name': None,
            'prod_suggestions': prod_results
        }
    ]

    return json.dumps(suggestions)


def recommend_from_random(db, Products, data):
    req_sex = data['sex']
    try:
        prev_prod_ids = data['prev_prod_ids']
    except:
        prev_prod_ids = None
    print(f'req_sex = {req_sex}')
    rand_conds = []
    rand_conds.append(
        and_(
            (Products.price > 40),
            (Products.price < 100)
        )
    )
    rand_conds.append(
        (Products.prod_id.isnot(None))
    )
    rand_conds.append(
        (Products.is_old.isnot(True))
    )
    rand_conds.append(
        Products.is_deleted.isnot(True)
    )
    if prev_prod_ids is not None:
        for prev_prod_id in prev_prod_ids:
            rand_conds.append(
                Products.prod_id != prev_prod_id
            )

    query = db.session.query(Products).filter(
        and_(*rand_conds)
    )

    query_results = query.order_by(func.random()).limit(40).all()
    prod_results = []
    for query_result in query_results:
        if len(query_result.image_urls) > 0:
            prod_serial = ProductsSchema().dump(query_result)
            prod_results.append(prod_serial)

    suggestions = [
        {
            'look_name': None,
            'prod_suggestions': prod_results
        }
    ]

    return json.dumps(suggestions)


def onboarding_recommend(db, ImagesSkinny, data):
    req_sex = data['sex']
    exception_cats = [
        'backpack',
        'bag',
        'beachwear',
        'belt',
        'bikini',
        'bodysuit',
        'bottom',
        'bra',
        'bralet',
        'bralette',
        'brief',
        'card holder',
        'handbag',
        'knickers',
        'lingerie',
        'lipstick',
        'makeup',
        'mamalicious',
        'maternity',
        'swim',
        'swimming',
        'swimsuit',
        'swimwear',
        'thong',
        'tote',
        'underwear',
        'watch',
        'watches'
    ]
    rand_conds = []
    rand_conds.append(
        (ImagesSkinny.prod_id.isnot(None))
    )
    rand_conds.append(
        ImagesSkinny.is_deleted.isnot(True)
    )

    query = db.session.query(ImagesSkinny).filter(
        and_(*rand_conds)
    )
    query_results = query.order_by(func.random()).limit(100).all()

    recommend_results = []
    prod_check = set()
    for query_result in query_results:
        prod_hash = query_result.prod_id
        if prod_hash not in prod_check and len(recommend_results) < 6:
            prod_check.add(prod_hash)
            contains_except = False
            for exception_cat in exception_cats:
                if exception_cat in query_result.name.lower():
                    contains_except = True

            if contains_except == False:
                img_serial = ImagesSkinnySchema().dump(query_result)
                recommend_results.append(img_serial)

    suggestions = {
            'look_name': None,
            'prod_suggestions': recommend_results
        }

    return json.dumps(suggestions)
