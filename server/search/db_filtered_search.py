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
import cv2


def calc_chi_distance(hist_1, hist_2, eps=1e-10):
    # compute the chi-squared distance
    distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_1, hist_2)])

    return distance


def calc_cross_entropy(vector_1, vector_2):
    dist = np.sum(vector_1 * np.log(vector_2) + (1 - vector_1) * np.log(1 - vector_2))

    return dist


def compare_histograms_int(arr_1, arr_2):
    arr_1_float = arr_1.astype(np.float32)
    arr_2_float = arr_2.astype(np.float32)
    distance = cv2.compareHist(arr_1_float, arr_2_float, cv2.HISTCMP_BHATTACHARYYA)
    return distance


def similar_image_histogram_search(request, db, ImagesFull, ImagesSkinny):
    data = request.get_json(force=True)
    data = json.loads(data)
    req_img_hash = data['img_hash']
    print(f'Req IMG HASH: {req_img_hash}')
    req_tags_positive = data['tags_positive']
    req_tags_negative = data['tags_negative']
    max_price = int(data['max_price'])
    print(f'max_price: {max_price}')
    req_brands = data['brands']
    initial_req = data['initial_req']
    discount_rate = data['discount_rate']
    print(f'discount_rate: {discount_rate}')
    try:
        prev_prod_ids = data['prev_prod_ids']
    except:
        prev_prod_ids = []
    search_limit = 1000

    print(f'req_tags_positive: {req_tags_positive}')

    req_image_data = ImagesFull.query.filter_by(img_hash=req_img_hash).first()
    if req_tags_positive is None:
        req_tags_positive = req_image_data.all_cats

    req_vgg16_enc = req_image_data.encoding_vgg16
    req_color_hist = req_image_data.color_hist
    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    length_cats = tag_list.length_cats
    pattern_cats = tag_list.pattern_cats
    material_cats = tag_list.material_cats
    style_cats = tag_list.style_cats
    all_cats = tag_list.all_cats
    kind_cats_search = []
    length_cats_search = []
    pattern_cats_search = []
    material_cats_search = []
    style_cats_search = []
    rest_cats_search = []

    if initial_req:
        kind_cats_search = [req_tag for req_tag in req_tags_positive if req_tag in kind_cats]
        if len(kind_cats_search) == 0:
            kind_cats_search = [req_tag for req_tag in req_image_data.kind_cats if req_tag in kind_cats]
        rest_of_cats = [cat for cat in req_image_data.all_cats if cat not in kind_cats and cat in all_cats]
        response_cats = kind_cats_search + rest_of_cats
        for word in rest_of_cats:
            for cat in length_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    length_cats_search.append(cat)
            for cat in pattern_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    pattern_cats_search.append(cat)
            for cat in material_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    material_cats_search.append(cat)
            for cat in style_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    style_cats_search.append(cat)
            if word not in kind_cats_search and word not in length_cats_search and word not in pattern_cats_search and word not in material_cats_search and word not in style_cats_search:
                rest_cats_search.append(word)
    else:
        response_cats = req_tags_positive
        for word in req_tags_positive:
            for cat in kind_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    kind_cats_search.append(cat)
            for cat in length_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    length_cats_search.append(cat)
            for cat in pattern_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    pattern_cats_search.append(cat)
            for cat in material_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    material_cats_search.append(cat)
            for cat in style_cats:
                if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
                    style_cats_search.append(cat)
            if word not in kind_cats_search and word not in length_cats_search and word not in pattern_cats_search and word not in material_cats_search and word not in style_cats_search:
                rest_cats_search.append(word)

    kind_cats_search = list(set(kind_cats_search[:3]))
    length_cats_search = list(set(length_cats_search))
    pattern_cats_search = list(set(pattern_cats_search))
    material_cats_search = list(set(material_cats_search))
    style_cats_search = list(set(style_cats_search))
    rest_cats_search = list(set(rest_cats_search))
    print('kind cats')
    print(kind_cats_search)
    print('length cats')
    print(length_cats_search)
    print('pattern cats')
    print(pattern_cats_search)
    print('material cats')
    print(material_cats_search)
    print('style cats')
    print(style_cats_search)
    print('rest of cats')
    print(rest_cats_search)
    query_conditions = []
    query_conds_cats_kind = []
    query_conds_cats_length = []
    query_conds_cats_pattern = []
    query_conds_cats_material = []
    query_conds_cats_style = []
    query_conds_cats_rest = []

    maternity_tags = ['mom', 'mum', 'mamalicious', 'maternity']
    is_maternity = False

    for req_tag_positive in rest_cats_search:
        query_conds_cats_rest.append(
            ImagesSkinny.name.ilike('%{}%'.format(req_tag_positive))
        )
        if req_tag_positive in maternity_tags:
            is_maternity = True

    for kind_search_cat in kind_cats_search:
        query_conds_cats_kind.append(
            (ImagesSkinny.kind_cats.any(kind_search_cat))
        )
    for length_search_cat in length_cats_search:
        query_conds_cats_length.append(
            (ImagesSkinny.length_cats.any(length_search_cat))
        )
    for pattern_search_cat in pattern_cats_search:
        query_conds_cats_pattern.append(
            (ImagesSkinny.pattern_cats.any(pattern_search_cat))
        )
    for material_search_cat in material_cats_search:
        query_conds_cats_material.append(
            (ImagesSkinny.material_cats.any(material_search_cat))
        )
    for style_search_cat in style_cats_search:
        query_conds_cats_style.append(
            (ImagesSkinny.style_cats.any(style_search_cat))
        )
    for tag in req_tags_negative:
        query_conditions.append(
            (~ImagesSkinny.name.ilike('%{}%'.format(tag)))
        )
    if is_maternity is False:
        for maternity_tag in maternity_tags:
            query_conditions.append(
                (~ImagesSkinny.name.ilike('%{}%'.format(maternity_tag)))
            )
    query_conditions.append(
        (ImagesSkinny.in_stock == True)
    )
    query_conditions.append(
        (ImagesSkinny.is_deleted is not True)
    )
    query_conditions.append(
        (ImagesFull.encoding_vgg16.isnot(None))
    )
    if discount_rate > 0:
        query_conditions.append(
            (ImagesSkinny.discount_rate >= discount_rate)
        )

    if len(req_brands) > 0:
        for req_brand in req_brands:
            req_brand_lower = req_brand.lower()
            query_conditions.append(
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
    for prev_prod_id in prev_prod_ids:
        query_conditions.append(
            ImagesSkinny.prod_id != prev_prod_id
        )

    query_results = db.session.query(ImagesSkinny, ImagesFull).filter(
        ImagesSkinny.img_hash == ImagesFull.img_hash
    ).filter(
        and_(
            and_(*query_conditions),
            and_(*query_conds_cats_kind),
            or_(*query_conds_cats_length),
            or_(*query_conds_cats_pattern),
            or_(*query_conds_cats_material),
            or_(*query_conds_cats_style),
            or_(*query_conds_cats_rest)
        )
    ).limit(search_limit).all()
    print(f'MAIN QUERY RESULT LENGTH: {len(query_results)}')

    if len(query_results) < 50:
        relaxed_query_results = db.session.query(ImagesSkinny, ImagesFull).filter(
            ImagesSkinny.img_hash == ImagesFull.img_hash
        ).filter(
            and_(
                and_(*query_conditions),
                and_(*query_conds_cats_kind),
                or_(*query_conds_cats_length)
            )
        ).limit(search_limit).all()
        query_results += relaxed_query_results
    print(f'TOTAL QUERY RESULT LENGTH: {len(query_results)}')

    query_results = [
        query_result for query_result in query_results if len(query_result[1].encoding_vgg16) == 512 and query_result[1].color_hist is not None
    ]

    if len(query_results) == 0:
        return [], response_cats, req_img_hash
    else:
        if len(query_results) > 300:
            closest_color_limit = int(len(query_results) / 3)
            closest_enc_limit = int(len(query_results) / 4)
        else:
            closest_color_limit = int(len(query_results) * 0.8)
            closest_enc_limit = int(len(query_results) * 0.6)

        target_encoding_arr = np.asarray(req_vgg16_enc)
        print(f'target_encoding_arr shape: {target_encoding_arr.shape}')
        target_hist_arr = np.asanyarray(req_color_hist)
        print(f'target_hist_arr shape: {target_hist_arr.shape}')

        color_hist_list = []
        vgg16_enc_list = []

        for query_result in query_results:
            color_hist_list.append(query_result[1].color_hist)

        color_hist_matrix = np.array(color_hist_list)

        print(f'len(color_hist_matrix): {len(color_hist_matrix)}')

        print('color_hist_matrix.shape')
        print(color_hist_matrix.shape)

        hist_dist_mtx = np.apply_along_axis(compare_histograms_int, 1, color_hist_matrix, target_hist_arr)

        # print('len(req_vgg16_enc)')
        # print(len(req_vgg16_enc))
        # target_encoding_arr = np.asarray(req_vgg16_enc)
        # euclidean_factor = 5000 if np.sum(target_color_arr) > 250 else 2000
        #
        # color_distances_1 = 1 - np.dot(color_1_matrix / norm(color_1_matrix, axis=1, keepdims=True),
        #                                (target_color_matrix / norm(target_color_matrix, axis=1, keepdims=True)).T)
        # color_distances_2 = 1 - np.dot(color_2_matrix / norm(color_2_matrix, axis=1, keepdims=True),
        #                                (target_color_matrix / norm(target_color_matrix, axis=1, keepdims=True)).T)
        # color_distances_3 = 1 - np.dot(color_3_matrix / norm(color_3_matrix, axis=1, keepdims=True),
        #                                (target_color_matrix / norm(target_color_matrix, axis=1, keepdims=True)).T)
        #
        # color_distances_1_mean = np.mean(color_distances_1, axis=1)
        # color_distances_2_mean = np.mean(color_distances_2, axis=1)
        # color_distances_3_mean = np.mean(color_distances_3, axis=1)
        #
        # # print(np.max(color_distances_1_mean))
        # # print(np.median(color_distances_1_mean))
        #
        # color_dist_1_euc = np.linalg.norm(color_1_matrix - target_color_arr, axis=1)
        # color_dist_2_euc = np.linalg.norm(color_2_matrix - target_color_arr, axis=1)
        # color_dist_3_euc = np.linalg.norm(color_3_matrix - target_color_arr, axis=1)
        #
        # # print(np.max((color_dist_1_euc / 5000)))
        # # print(np.median((color_dist_1_euc / 5000)))
        #
        # color_distances_1_combined = color_distances_1_mean + (color_dist_1_euc / euclidean_factor)
        # color_distances_2_combined = color_distances_2_mean + (color_dist_2_euc / euclidean_factor)
        # color_distances_3_combined = color_distances_3_mean + (color_dist_3_euc / euclidean_factor)
        #
        # color_dist_intm = np.add(color_distances_1_combined, color_distances_2_combined * 0.7)
        # color_dist_total = np.add(color_dist_intm, color_distances_3_combined * 0.4)
        closest_color_idx = hist_dist_mtx.argsort()[0:closest_color_limit]
        closest_n_results_color = [{
            'query_result': query_results[idx][1],
            'color_dist': hist_dist_mtx[idx]
        } for idx in closest_color_idx]
        print(f'Closest colors calculated, length: {len(closest_n_results_color)}')

        for query_result_dict in closest_n_results_color:
            vgg16_enc_list.append(query_result_dict['query_result'].encoding_vgg16)
        vgg16_enc_matrix = np.array(vgg16_enc_list)

        dist_encoding_arr = np.linalg.norm(vgg16_enc_matrix - target_encoding_arr, axis=1)
        closest_n_enc_ind = dist_encoding_arr.argsort()[0:closest_enc_limit]
        closest_n_results_enc = [closest_n_results_color[x] for x in closest_n_enc_ind]
        print(f'Closest encodings calculated, length: {len(closest_n_results_enc)}')

        top_encoding_list = sorted(closest_n_results_enc, key=itemgetter('color_dist'))
        top_encoding_list = top_encoding_list[0:60]

        if len(prev_prod_ids) == 0:
            # Make sure we return the original request image back on top
            if not any(d['query_result'].img_hash == req_img_hash for d in closest_n_results_enc):
                print('Product not in list, need to add')
                top_encoding_list.insert(0, {
                    'query_result': req_image_data,
                    'color_dist': 0
                })
            else:
                print('Product already in list, need to make sure its on top')
                request_prod_idx = next((index for (index, d) in enumerate(closest_n_results_enc) if d['query_result'].img_hash == req_img_hash), None)
                del closest_n_results_enc[request_prod_idx]
                top_encoding_list.insert(0, {
                    'query_result': req_image_data,
                    'color_dist': 0
                })

        # Serialize the results and return as array
        result_list = []
        prod_check = set()
        print('Obtaining result data')
        for result_dict in top_encoding_list:
            img_query_result = result_dict['query_result']
            # result_prod_id = img_query_result.prod_id
            # prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
            # if prod_search is not None:
            prod_hash = img_query_result.prod_id
            if prod_hash not in prod_check:
                # prod_serial = ProductsSchema().dump(prod_search)
                prod_check.add(prod_hash)
                img_serial = ImagesFullSchema().dump(img_query_result)
                # print(img_serial)
                result_dict = {
                    'prod_serial': [],
                    'image_data': img_serial[0]
                }
                result_list.append(result_dict)

        return result_list, response_cats, req_img_hash
