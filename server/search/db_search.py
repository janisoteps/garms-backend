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


def calc_cross_entropy(vector_1, vector_2):
    dist = np.sum(vector_1 * np.log(vector_2) + (1 - vector_1) * np.log(1 - vector_2))

    return dist


# def search_similar_images(request, db, Images, ImagesSkinny, Products):
#     data = request.get_json(force=True)
#     data = json.loads(data)
#     req_img_hash = data['img_hash']
#     req_tags_positive = data['tags_positive']
#     req_tags_negative = data['tags_negative']
#     req_color_1 = data['color_1']
#     req_sex = data['sex']
#     max_price = int(data['max_price'])
#     req_brands = data['brands']
#     discount_rate = data['discount_rate']
#
#     req_image_data = Images.query.filter_by(img_hash=req_img_hash).first()
#
#     result_limit = 2000
#
#     print('RGB 1: ', str(req_color_1))
#     print(f'Positive tags: {req_tags_positive}')
#     print(f'Negative tags: {req_tags_negative}')
#
#     if req_tags_positive is None:
#         req_tags_positive = req_image_data.all_cats
#
#     req_tags_positive = list(set(req_tags_positive))
#
#     print(f'Updated Positive tags: {req_tags_positive}')
#     search_string_clean = ' '.join(req_tags_positive)
#
#     tag_list = cats.Cats()
#     kind_cats = tag_list.kind_cats
#     pattern_cats = tag_list.pattern_cats
#     color_cats = tag_list.color_cats
#     style_cats = tag_list.style_cats
#     material_cats = tag_list.material_cats
#     attribute_cats = tag_list.attribute_cats
#     length_cats = tag_list.length_cats
#     filter_cats = tag_list.filter_cats
#     all_cats = tag_list.all_cats
#
#     kind_cats_search = []
#     pattern_cats_search = []
#     color_cats_search = []
#     style_cats_search = []
#     material_cats_search = []
#     attribute_cats_search = []
#     length_cats_search = []
#     filter_cats_search = []
#     all_cats_search = []
#
#     for word in req_tags_positive:
#         for cat in kind_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 kind_cats_search.append(cat)
#         for cat in pattern_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 pattern_cats_search.append(cat)
#         for cat in color_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 color_cats_search.append(cat)
#         for cat in style_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 style_cats_search.append(cat)
#         for cat in material_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 material_cats_search.append(cat)
#         for cat in attribute_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 attribute_cats_search.append(cat)
#         for cat in length_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 length_cats_search.append(cat)
#         for cat in filter_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 filter_cats_search.append(cat)
#         for cat in all_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
#                 all_cats_search.append(cat)
#
#     print('kind_cats_search')
#     print(kind_cats_search)
#     print('pattern_cats_search')
#     print(pattern_cats_search)
#     print('color_cats_search')
#     print(color_cats_search)
#     print('style_cats_search')
#     print(style_cats_search)
#     print('material_cats_search')
#     print(material_cats_search)
#     print('attribute_cats_search')
#     print(attribute_cats_search)
#     print('length_cats_search')
#     print(length_cats_search)
#     print('filter_cats_search')
#     print(filter_cats_search)
#     print('all_cats_search')
#     print(all_cats_search)
#
#     print('Assembling db query conditions')
#     conditions_base = []
#     conditions_kind_cats = []
#     conditions_pattern_cats = []
#     conditions_color_cats = []
#     conditions_style_cats = []
#     conditions_material_cats = []
#     conditions_attribute_cats = []
#     conditions_length_cats = []
#     conditions_filter_cats = []
#     conditions_all_cats = []
#
#     conditions_brand = []
#     query_conditions_all = []
#     query_conditions_no_results = []
#
#     for tag in req_tags_positive:
#         conditions_all_cats.append(
#             (ImagesSkinny.all_cats.any(tag))
#         )
#
#     for kind_search_cat in kind_cats_search:
#         conditions_kind_cats.append(
#             (ImagesSkinny.kind_cats.any(kind_search_cat))
#         )
#
#     if req_sex == 'women':
#         for pattern_search_cat in pattern_cats_search:
#             conditions_pattern_cats.append(
#                 (ImagesSkinny.pattern_cats.any(pattern_search_cat))
#             )
#
#         for color_search_cat in color_cats_search:
#             conditions_color_cats.append(
#                 (ImagesSkinny.color_cats.any(color_search_cat))
#             )
#
#     for style_search_cat in style_cats_search:
#         conditions_style_cats.append(
#             (ImagesSkinny.style_cats.any(style_search_cat))
#         )
#
#     for material_search_cat in material_cats_search:
#         conditions_material_cats.append(
#             (ImagesSkinny.material_cats.any(material_search_cat))
#         )
#
#     for attribute_search_cat in attribute_cats_search:
#         conditions_attribute_cats.append(
#             (ImagesSkinny.attribute_cats.any(attribute_search_cat))
#         )
#
#     if req_sex == 'women':
#         for length_search_cat in length_cats_search:
#             conditions_length_cats.append(
#                 (ImagesSkinny.length_cats.any(length_search_cat))
#             )
#
#     for filter_search_cat in filter_cats_search:
#         conditions_filter_cats.append(
#             (ImagesSkinny.filter_cats.any(filter_search_cat))
#         )
#
#     for tag in req_tags_negative:
#         print(f'negative tag: {tag}')
#         conditions_base.append(
#             (~ImagesSkinny.all_cats.any(tag))
#         )
#
#     if len(req_sex) > 2:
#         conditions_base.append(
#             (ImagesSkinny.sex == req_sex)
#         )
#
#     if len(req_brands) > 0:
#         for req_brand in req_brands:
#             conditions_brand.append(
#                 (ImagesSkinny.brand == req_brand)
#             )
#             conditions_brand.append(
#                 (ImagesSkinny.brand.ilike('%{0}%'.format(req_brand)))
#             )
#         print('filtering for brands')
#         print(req_brands)
#
#     if max_price < 1000000:
#         conditions_base.append(
#             or_((ImagesSkinny.price < max_price),
#                 and_((ImagesSkinny.sale == True), (ImagesSkinny.saleprice < max_price)))
#         )
#     conditions_base.append(
#         (ImagesSkinny.in_stock == True)
#     )
#     conditions_base.append(
#         (Images.encoding_vgg16 != None)
#     )
#     query_conditions_all.append(
#         (func.lower(ImagesSkinny.name).op('%%')(search_string_clean))
#     )
#     query_conditions_no_results.append(
#         func.lower(ImagesSkinny.name).op('@@')(func.plainto_tsquery(search_string_clean))
#     )
#     conditions_base.append(
#         (ImagesSkinny.discount_rate > discount_rate)
#     )
#
#     # ====== MAIN QUERY ======
#     img_table_query_results = (db.session.query(ImagesSkinny, Images).filter(
#         ImagesSkinny.img_hash == Images.img_hash
#     ).filter(
#         and_(
#             and_(*conditions_base),
#             and_(*conditions_kind_cats),
#             or_(*conditions_pattern_cats),
#             or_(*conditions_color_cats),
#             or_(*conditions_style_cats),
#             or_(*conditions_material_cats),
#             or_(*conditions_attribute_cats),
#             and_(*conditions_length_cats),
#             and_(*conditions_filter_cats),
#             or_(*conditions_brand)
#         )
#     ).limit(result_limit).all())
#
#     print(f'RESULT LENGTH: {len(img_table_query_results)}')
#
#     if len(img_table_query_results) < 500:
#         print('ADDING RELAXED RESULTS')
#         query_results_relaxed = (db.session.query(ImagesSkinny, Images).filter(
#             ImagesSkinny.img_hash == Images.img_hash
#         ).filter(
#             and_(
#                 and_(*conditions_base),
#                 and_(*conditions_kind_cats),
#                 or_(*conditions_pattern_cats),
#                 or_(*conditions_style_cats),
#                 or_(*conditions_length_cats),
#                 or_(*conditions_filter_cats),
#                 or_(*conditions_brand)
#             )
#         ).limit(1000 - len(img_table_query_results)).all())
#         print(f'{len(query_results_relaxed)} RELAXED RESULTS ADDED')
#         img_table_query_results += query_results_relaxed
#
#     if len(img_table_query_results) < 200:
#         print('ADDING EVEN MORE RELAXED RESULTS')
#         query_results_relaxed_2 = (db.session.query(ImagesSkinny, Images).filter(
#             ImagesSkinny.img_hash == Images.img_hash
#         ).filter(
#             and_(
#                 and_(*conditions_base),
#                 and_(*conditions_kind_cats),
#                 or_(*query_conditions_all),
#                 or_(*conditions_filter_cats),
#                 or_(*conditions_brand)
#             )
#         ).limit(1000 - len(img_table_query_results)).all())
#         print(f'{len(query_results_relaxed_2)} MORE RELAXED RESULTS ADDED')
#         img_table_query_results += query_results_relaxed_2
#
#     if len(img_table_query_results) < 100:
#         print('ADDING EVEN MORE RELAXED RESULTS')
#         query_results_relaxed_3 = (db.session.query(ImagesSkinny, Images).filter(
#             ImagesSkinny.img_hash == Images.img_hash
#         ).filter(
#             and_(
#                 and_(*conditions_base),
#                 or_(*conditions_kind_cats),
#                 or_(*conditions_brand)
#             )
#         ).limit(1000 - len(img_table_query_results)).all())
#
#         print(f'{len(query_results_relaxed_3)} MORE RELAXED RESULTS ADDED')
#
#         img_table_query_results += query_results_relaxed_3
#
#     if len(img_table_query_results) < 100:
#         query_results_relaxed_4 = (db.session.query(ImagesSkinny, Images).filter(
#             ImagesSkinny.img_hash == Images.img_hash
#         ).filter(
#             and_(*query_conditions_no_results)
#         ).limit(1000 - len(img_table_query_results)).all())
#
#         print(f'{len(query_results_relaxed_4)} LAST RESORT RESULTS ADDED')
#
#         img_table_query_results += query_results_relaxed_4
#
#     # req_encoding_crop = req_image_data.encoding_crop
#     req_encoding_vgg16 = req_image_data.encoding_vgg16
#
#     # Start with main RBG color distances to reduce the amount of the rest of the distances to calc
#     print(f'TOTAL RESULT LENGTH: {len(img_table_query_results)}')
#     if len(img_table_query_results) == 0:
#         return False
#
#     color_list = []
#     for img_table_query_result in img_table_query_results:
#         query_result = img_table_query_result[1]
#         try:
#             image_prod_name = query_result.name
#             vgg_16_len = len(query_result.encoding_vgg16)
#         except:
#             image_prod_name = None
#             vgg_16_len = 0
#         if image_prod_name is not None and vgg_16_len == 4096:
#             image_prod_name_arr = image_prod_name.lower().strip('*\'[]\*').split(' ')
#
#             neg_tag_check = False
#             for neg_tag in req_tags_negative:
#                 neg_tag_check = neg_tag in image_prod_name_arr
#
#             if neg_tag_check is False:
#                 req_color_norm_1 = np.array(req_color_1, dtype=int) / np.sum(np.array(req_color_1, dtype=int))
#
#                 query_color_1_norm = np.array(query_result.color_1, dtype=int) / np.sum(
#                     np.array(query_result.color_1, dtype=int))
#                 query_color_2_norm = np.array(query_result.color_2, dtype=int) / np.sum(
#                     np.array(query_result.color_2, dtype=int))
#                 query_color_3_norm = np.array(query_result.color_3, dtype=int) / np.sum(
#                     np.array(query_result.color_3, dtype=int))
#
#                 # compute the chi-squared distances
#                 distance_color_1 = calc_chi_distance(req_color_norm_1, query_color_1_norm)
#                 distance_color_2 = calc_chi_distance(req_color_norm_1, query_color_2_norm)
#                 distance_color_3 = calc_chi_distance(req_color_norm_1, query_color_3_norm)
#
#                 distance_color = 10 * distance_color_1 + 3 * distance_color_2 + distance_color_3
#
#                 distance_color_euc_1 = int(
#                     spatial.distance.euclidean(np.array(req_color_1, dtype=int),
#                                                np.array(query_result.color_1, dtype=int),
#                                                w=None))
#                 distance_color_euc_2 = int(
#                     spatial.distance.euclidean(np.array(req_color_1, dtype=int),
#                                                np.array(query_result.color_2, dtype=int),
#                                                w=None))
#                 distance_color_euc_3 = int(
#                     spatial.distance.euclidean(np.array(req_color_1, dtype=int),
#                                                np.array(query_result.color_3, dtype=int),
#                                                w=None))
#
#                 distance_color_euc = (1 / 500) * min([
#                     distance_color_euc_1,
#                     distance_color_euc_2,
#                     distance_color_euc_3
#                 ])
#
#                 color_query_result = {
#                     'query_result': query_result,
#                     'img_hash': query_result.img_hash,
#                     'prod_id': query_result.prod_id,
#                     'color_dist': distance_color_euc + distance_color
#                 }
#                 color_list.append(color_query_result)
#
#     sorted_color_list = sorted(color_list, key=itemgetter('color_dist'))
#     top_color_list = sorted_color_list[0:int(result_limit * 0.5)]
#
#     # CALCULATE ENCODING DISTANCES
#     encoding_arrays = []
#     for query_result in top_color_list:
#         encoding_arrays.append(query_result['query_result'].encoding_vgg16)
#     encoding_matrix = np.asarray(encoding_arrays)
#
#     dist_encoding_arr = np.linalg.norm(encoding_matrix - req_encoding_vgg16, axis=1)
#     closest_n_enc_ind = dist_encoding_arr.argsort()[:100]
#     closest_n_enc_results = [top_color_list[x] for x in closest_n_enc_ind]
#     print(f'Closest encodings calculated, length: {len(closest_n_enc_results)}')
#
#     # Make sure we return the original request image back on top
#     if not any(d['img_hash'] == req_img_hash for d in closest_n_enc_results):
#         print('Product not in list, need to add')
#         closest_n_enc_results.insert(0, {
#             'img_hash': req_img_hash,
#             'prod_id': req_image_data.prod_id,
#             'query_result': req_image_data,
#             'encoding_crop_dist': -1000,
#             'color_dist': -1000
#         })
#     else:
#         print('Product already in list, need to make sure its on top')
#         request_prod = next(item for item in closest_n_enc_results if item['img_hash'] == req_img_hash)
#         request_prod['color_dist'] = -1000
#         request_prod['encoding_crop_dist'] = -1000
#
#     top_encoding_list = sorted(closest_n_enc_results, key=itemgetter('color_dist'))
#     top_encoding_list = top_encoding_list[0:50]
#
#     # Serialize the results and return as array
#     result_list = []
#     prod_check = set()
#     print('Obtaining result data')
#     for obj in top_encoding_list:
#         result_prod_id = obj['prod_id']
#         prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
#         if prod_search is not None:
#             prod_hash = prod_search.prod_id
#             if prod_hash not in prod_check:
#                 prod_serial = ProductsSchema().dump(prod_search)
#                 prod_check.add(prod_hash)
#                 img_serial = ImagesFullSchema().dump(obj['query_result'])
#                 result_dict = {
#                     'prod_serial': prod_serial[0],
#                     'image_data': img_serial[0]
#                 }
#                 result_list.append(result_dict)
#
#     return result_list


#######################################################################################################################
#######################################################################################################################


def infinite_similar_images(request, db, ImagesFull, ImagesSkinny, Products):
    data = request.get_json(force=True)
    data = json.loads(data)
    req_img_hash = data['img_hash']
    print(f'Req IMG HASH: {req_img_hash}')
    req_tags_positive = data['tags_positive']
    req_tags_negative = data['tags_negative']
    req_color_1 = data['color_1']
    print(f'req_color_1: {req_color_1}')
    req_sex = data['sex']
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
    if len(req_color_1) == 0:
        # color_list = [req_image_data.color_1, req_image_data.color_2, req_image_data.color_3]
        # color_sums = [sum(color) for color in color_list]
        req_color_1 = req_image_data.color_1

    req_vgg16_enc = req_image_data.encoding_vgg16
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

    query_results = [query_result for query_result in query_results if len(query_result[1].encoding_vgg16) == 512]

    if len(query_results) == 0:
        return [], response_cats, list(req_color_1), req_img_hash
    else:
        if len(query_results) > 300:
            closest_color_limit = int(len(query_results) / 2)
            closest_enc_limit = int(len(query_results) / 3)
        else:
            closest_color_limit = len(query_results)
            closest_enc_limit = len(query_results)

        color_1_list = []
        color_2_list = []
        color_3_list = []
        vgg16_enc_list = []

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
        target_color_matrix = np.broadcast_to(np.array(req_color_1), color_1_matrix.shape)
        target_color_arr = np.asarray(req_color_1)

        print('len(req_vgg16_enc)')
        print(len(req_vgg16_enc))
        target_encoding_arr = np.asarray(req_vgg16_enc)
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

        # print(np.max(color_distances_1_mean))
        # print(np.median(color_distances_1_mean))

        color_dist_1_euc = np.linalg.norm(color_1_matrix - target_color_arr, axis=1)
        color_dist_2_euc = np.linalg.norm(color_2_matrix - target_color_arr, axis=1)
        color_dist_3_euc = np.linalg.norm(color_3_matrix - target_color_arr, axis=1)

        # print(np.max((color_dist_1_euc / 5000)))
        # print(np.median((color_dist_1_euc / 5000)))

        color_distances_1_combined = color_distances_1_mean + (color_dist_1_euc / euclidean_factor)
        color_distances_2_combined = color_distances_2_mean + (color_dist_2_euc / euclidean_factor)
        color_distances_3_combined = color_distances_3_mean + (color_dist_3_euc / euclidean_factor)

        color_dist_intm = np.add(color_distances_1_combined, color_distances_2_combined * 0.7)
        color_dist_total = np.add(color_dist_intm, color_distances_3_combined * 0.4)
        closest_color_idx = color_dist_total.argsort()[0:closest_color_limit]
        closest_n_results_color = [{
            'query_result': query_results[idx][1],
            'color_dist': color_dist_total[idx]
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

        return result_list, response_cats, list(req_color_1), req_img_hash


#######################################################################################################################
#######################################################################################################################


def db_test_search(request, db, ImagesV2, ImagesV2Skinny, ProductsV2):
    data = request.get_json(force=True)
    # data = json.loads(data)

    sex = data['sex']
    tags = data['tags']

    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    style_cats = tag_list.style_cats
    filter_cats = tag_list.filter_cats
    length_cats = tag_list.length_cats
    color_pattern_cats = tag_list.color_pattern_cats
    kind_search_cats = [req_tag for req_tag in tags if req_tag in kind_cats]
    style_search_cats = [req_tag for req_tag in tags if req_tag in style_cats]
    length_search_cats = [req_tag for req_tag in tags if req_tag in length_cats]
    color_pattern_search_cats = [req_tag for req_tag in tags if req_tag in color_pattern_cats]
    filter_search_cats = [req_tag for req_tag in tags if req_tag in filter_cats]

    print(f'KIND CATS: {kind_search_cats}')
    print(f'STYLE CATS: {style_search_cats}')
    print(f'LENGTH CATS: {length_search_cats}')
    print(f'COLOR PATTERN CATS: {color_pattern_search_cats}')
    print(f'FILTER CATS: {filter_search_cats}')

    query_conds = []

    for kind_search_cat in kind_search_cats:
        query_conds.append(
            (ImagesV2Skinny.kind_cats.any(kind_search_cat))
        )

    for style_search_cat in style_search_cats:
        query_conds.append(
            (ImagesV2Skinny.style_cats.any(style_search_cat))
        )

    for length_search_cat in length_search_cats:
        query_conds.append(
            (ImagesV2Skinny.all_cats.any(length_search_cat))
        )

    for color_pattern_search_cat in color_pattern_search_cats:
        query_conds.append(
            (ImagesV2Skinny.color_pattern_cats.any(color_pattern_search_cat))
        )

    for filter_search_cat in filter_search_cats:
        query_conds.append(
            (ImagesV2Skinny.filter_cats.any(filter_search_cat))
        )

    query_conds.append(
        (ImagesV2Skinny.sex == sex)
    )

    query_conds.append(
        (ImagesV2Skinny.in_stock == True)
    )
    query_conds.append(
        (ImagesV2.encoding_vgg16 != None)
    )

    img_table_query_results = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
        ImagesV2Skinny.img_hash == ImagesV2.img_hash
    ).filter(
        and_(*query_conds)
    ).limit(500).all())

    result_len = len(img_table_query_results)

    limited_query_results = img_table_query_results[:100]

    result_list = []
    for img_table_query_result in limited_query_results:
        query_result_skinny = img_table_query_result[0]

        result_prod_id = query_result_skinny.prod_id
        prod_search = db.session.query(ProductsV2).filter(ProductsV2.prod_id == result_prod_id).first()
        prod_serial = ProductsSchema().dump(prod_search)

        result_dict = {
            'count': result_len,
            'prod_serial': prod_serial[0]
        }
        result_list.append(result_dict)

    return result_list

