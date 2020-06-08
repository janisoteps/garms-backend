from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ImagesFullSchema, ProductsSchema
import scipy.spatial as spatial
import numpy as np
from numpy.linalg import norm
from operator import itemgetter
import json
from flask import jsonify
import data.cats as cats
import data.colors as colors


def calc_chi_distance(hist_1, hist_2, eps=1e-10):
    # compute the chi-squared distance
    distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_1, hist_2)])

    return distance


def db_text_search_infinite_v2(data, db, Products, Images, ImagesSkinny):
    search_string = data['search_string']
    req_sex = data['sex']
    prev_prod_ids = data['prev_prod_ids']
    discount_rate = data['discount_rate']
    search_limit = 100
    tag_list = cats.Cats()
    query_conditions = []
    query_conds_all_cats = []
    all_cats = tag_list.all_cats
    all_cats_search = []
    string_list = search_string.strip().lower().split()
    search_string_clean = ' '.join(string_list)

    print(f'search_string: {search_string_clean}')
    for word in string_list:
        for cat in all_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                all_cats_search.append(cat)

    for cat_search in all_cats_search:
        query_conds_all_cats.append(
            ImagesSkinny.all_cats.any(cat_search)
            # ImagesSkinny.name.ilike('%{}%'.format(cat_search))
        )

    for clean_string in string_list:
        query_conditions.append(
            ImagesSkinny.name.ilike('%{}%'.format(clean_string))
        )
    query_conditions.append(
        ImagesSkinny.is_deleted.isnot(True)
    )
    query_conds_all_cats.append(
        ImagesSkinny.is_deleted.isnot(True)
    )
    query_conditions.append(
        (ImagesSkinny.discount_rate >= discount_rate)
    )

    if prev_prod_ids is not None:
        for prev_prod_id in prev_prod_ids:
            query_conditions.append(
                ImagesSkinny.prod_id != prev_prod_id
            )
            query_conds_all_cats.append(
                ImagesSkinny.prod_id != prev_prod_id
            )

    query_results = db.session.query(ImagesSkinny, Images).filter(
            ImagesSkinny.img_hash == Images.img_hash
        ).filter(
            and_(*query_conds_all_cats)
        ).limit(search_limit).all()

    print(f'QUERY RESULT LENGTH: {len(query_results)}')
    if len(query_results) < 30:
        query_results_extended = db.session.query(ImagesSkinny, Images).filter(
        ImagesSkinny.img_hash == Images.img_hash
    ).filter(
        and_(*query_conditions)
    ).limit(search_limit).all()
        query_results += query_results_extended
    print(f'QUERY RESULT LENGTH: {len(query_results)}')

    result_list = []
    prod_check = set()
    for query_result in query_results:
        img_table_query_result = query_result[1]
        result_prod_id = img_table_query_result.prod_id
        # prod_id = query_result.prod_id
        if result_prod_id not in prod_check:
            # img_result = db.session.query(Images).filter(Images.prod_id == prod_id).first()
            prod_result = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
            if prod_result is not None:
                prod_serial = ProductsSchema().dump(prod_result)
                img_serial = ImagesFullSchema().dump(img_table_query_result)

                result_dict = {
                    'prod_serial': prod_serial[0],
                    'image_data': img_serial[0]
                }
                result_list.append(result_dict)
                prod_check.add(result_prod_id)

    res = jsonify(res=result_list, tags=all_cats_search)
    return res


def db_text_color_search(data, db, Images, ImagesSkinny):
    search_words = data['search_words']
    prev_prod_ids = data['prev_prod_ids']
    search_color = data['color']
    max_price = int(data['max_price'])
    req_brands = data['brands']
    discount_rate = data['discount_rate']
    print(f'discount_rate: {discount_rate}')
    search_limit = 2000
    result_limit = 100
    tag_list = cats.Cats()
    query_conditions = []
    query_conds_all_cats = []
    brand_conds = []
    all_cats = tag_list.all_cats
    all_cats_search = []
    string_list = [word.strip().lower() for word in search_words]
    print(f'SEARCH WORDS: {string_list}')

    color_rgb_dict = colors.Colors().color_rgb
    word_color = None
    for word in string_list:
        if word in color_rgb_dict:
            word_color = color_rgb_dict[word]
    if len(search_color) == 0 and word_color is not None:
        search_color = word_color

    # This is to avoid division by 0 error
    if len(search_color) > 0:
        search_color = [color + 1 for color in search_color]

    for word in string_list:
        for cat in all_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                all_cats_search.append(cat)

    for cat_search in all_cats_search:
        query_conds_all_cats.append(
            ImagesSkinny.all_cats.any(cat_search)
        )

    for clean_string in string_list:
        query_conditions.append(
            ImagesSkinny.name.ilike('%{}%'.format(clean_string))
        )
    query_conditions.append(
        ImagesSkinny.is_deleted.isnot(True)
    )
    query_conds_all_cats.append(
        ImagesSkinny.is_deleted.isnot(True)
    )
    if discount_rate > 0:
        print('applying discount filter')
        query_conditions.append(
            (ImagesSkinny.discount_rate >= discount_rate)
        )
        query_conds_all_cats.append(
            (ImagesSkinny.discount_rate >= discount_rate)
        )

    if prev_prod_ids is not None:
        for prev_prod_id in prev_prod_ids:
            query_conditions.append(
                ImagesSkinny.prod_id != prev_prod_id
            )
            query_conds_all_cats.append(
                ImagesSkinny.prod_id != prev_prod_id
            )

    if len(req_brands) > 0:
        for req_brand in req_brands:
            req_brand_lower = req_brand.lower()
            brand_conds.append(
                (func.lower(ImagesSkinny.brand).ilike('%{0}%'.format(req_brand_lower)))
            )

    if max_price < 1000000:
        query_conditions.append(
            or_(
                (ImagesSkinny.price < max_price),
                and_(
                    (ImagesSkinny.sale == True), (ImagesSkinny.saleprice < max_price)
                )
            )
        )
        query_conds_all_cats.append(
            or_(
                (ImagesSkinny.price < max_price),
                and_(
                    (ImagesSkinny.sale == True), (ImagesSkinny.saleprice < max_price)
                )
            )
        )

    query_results = db.session.query(ImagesSkinny, Images).filter(
        ImagesSkinny.img_hash == Images.img_hash
    ).filter(
        and_(
            and_(*query_conds_all_cats),
            or_(*brand_conds)
        )
    ).limit(search_limit).all()

    print(f'QUERY RESULT LENGTH: {len(query_results)}')
    if len(query_results) < 30:
        query_results_extended = db.session.query(ImagesSkinny, Images).filter(
            ImagesSkinny.img_hash == Images.img_hash
        ).filter(
            and_(
                and_(*query_conditions),
                or_(*brand_conds)
            )
        ).limit(search_limit).all()
        query_results += query_results_extended
    print(f'QUERY RESULT LENGTH: {len(query_results)}')

    if len(query_results) == 0:
        return []
    else:
        if len(search_color) == 0:
            # Serialize the results and return as array
            result_list = []
            prod_check = set()
            print('Obtaining result data')
            for query_result in query_results[:100]:
                img_query_result = query_result[1]
                prod_hash = img_query_result.prod_id
                if prod_hash not in prod_check:
                    prod_check.add(prod_hash)
                    img_serial = ImagesFullSchema().dump(img_query_result)
                    result_dict = {
                        'image_data': img_serial[0]
                    }
                    result_list.append(result_dict)
            return result_list

        else:
            color_1_list = []
            color_2_list = []
            color_3_list = []

            for query_result in query_results:
                color_1_list.append(query_result[1].color_1)
                color_2_list.append(query_result[1].color_2)
                color_3_list.append(query_result[1].color_3)

            color_1_matrix = np.array(color_1_list)
            color_2_matrix = np.array(color_2_list)
            color_3_matrix = np.array(color_3_list)

            print(len(color_1_list))
            print(len(color_2_list))
            print(len(color_3_list))

            print('color_1_matrix.shape')
            print(color_1_matrix.shape)
            target_color_matrix = np.broadcast_to(np.array(search_color), color_1_matrix.shape)
            target_color_arr = np.asarray(search_color)
            euclidean_factor = 5000 if np.sum(target_color_arr) > 250 else 2000

            color_distances_1 = 1 - np.dot(color_1_matrix / norm(color_1_matrix, axis=1, keepdims=True),
                                           (target_color_matrix / norm(target_color_matrix, axis=1, keepdims=True)).T)
            color_distances_2 = 1 - np.dot(color_2_matrix / norm(color_2_matrix, axis=1, keepdims=True),
                                           (target_color_matrix / norm(target_color_matrix, axis=1, keepdims=True)).T)
            color_distances_3 = 1 - np.dot(color_3_matrix / norm(color_3_matrix, axis=1, keepdims=True),
                                           (target_color_matrix / norm(target_color_matrix, axis=1, keepdims=True)).T)

            color_distances_1_mean = np.mean(color_distances_1, axis=1)
            color_distances_2_mean = np.mean(color_distances_2, axis=1)
            color_distances_3_mean = np.mean(color_distances_3, axis=1)

            color_dist_1_euc = np.linalg.norm(color_1_matrix - target_color_arr, axis=1)
            color_dist_2_euc = np.linalg.norm(color_2_matrix - target_color_arr, axis=1)
            color_dist_3_euc = np.linalg.norm(color_3_matrix - target_color_arr, axis=1)

            color_distances_1_combined = color_distances_1_mean + (color_dist_1_euc / euclidean_factor)
            color_distances_2_combined = color_distances_2_mean + (color_dist_2_euc / euclidean_factor)
            color_distances_3_combined = color_distances_3_mean + (color_dist_3_euc / euclidean_factor)

            color_dist_intm = np.add(color_distances_1_combined, color_distances_2_combined * 0.7)
            color_dist_total = np.add(color_dist_intm, color_distances_3_combined * 0.4)
            closest_color_idx = color_dist_total.argsort()[0:result_limit]

            closest_n_results_color = [{
                'query_result': query_results[idx][1],
                'color_dist': color_dist_total[idx]
            } for idx in closest_color_idx]
            print(f'Closest colors calculated, length: {len(closest_n_results_color)}')

            # Serialize the results and return as array
            result_list = []
            prod_check = set()
            print('Obtaining result data')
            for result_dict in closest_n_results_color:
                img_query_result = result_dict['query_result']
                prod_hash = img_query_result.prod_id
                if prod_hash not in prod_check:
                    prod_check.add(prod_hash)
                    img_serial = ImagesFullSchema().dump(img_query_result)
                    result_dict = {
                        'image_data': img_serial[0]
                    }
                    result_list.append(result_dict)

            # res = jsonify(res=result_list)
            return result_list
