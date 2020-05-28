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

#
# def db_text_search(request, db, Products, Images, ImagesSkinny):
#     search_string = request.args.get('search_string')
#     print('search string: ' + search_string)
#     search_string.replace('+', ' ')
#     req_sex = request.args.get('sex')
#
#     string_list = search_string.strip().lower().split()
#     linking_words = ['with', 'on', 'under', 'over', 'at', 'like', 'in', 'for', 'as', 'after', 'by', 'and']
#     string_list_clean = [e for e in string_list if e not in linking_words]
#     print('Cleaned string list', str(string_list_clean))
#     search_string_clean = ' '.join(string_list_clean)
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
#     all_cats_search = []
#     for word in string_list_clean:
#         for cat in all_cats:
#             if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                 all_cats_search.append(cat)
#
#     color_rgb_dict = colors.Colors().color_rgb
#     search_color = None
#     for word in string_list_clean:
#         if word in color_rgb_dict:
#             search_color = color_rgb_dict[word]
#             search_color = [color + 1 for color in search_color]
#
#     if search_color is not None:
#         search_limit = 1000
#         relaxed_threshold = 100
#         relaxed_limit = 500
#     else:
#         search_limit = 80
#         relaxed_threshold = 80
#         relaxed_limit = 80
#     if search_color is not None:
#         color_search_data = {
#             'search_words': string_list_clean,
#             'prev_prod_ids': [],
#             'color': search_color,
#             'max_price': 500,
#             'brands': []
#         }
#         result_list = db_text_color_search(color_search_data, db, Images, ImagesSkinny)
#         res = jsonify(res=result_list, tags=all_cats_search)
#         return res
#
#     else:
#         maternity = False
#         kind_cats_search = []
#         pattern_cats_search = []
#         color_cats_search = []
#         style_cats_search = []
#         material_cats_search = []
#         attribute_cats_search = []
#         length_cats_search = []
#         filter_cats_search = []
#
#         for word in string_list_clean:
#             for cat in kind_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     kind_cats_search.append(cat)
#             for cat in pattern_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     pattern_cats_search.append(cat)
#             for cat in color_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     color_cats_search.append(cat)
#             for cat in style_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     style_cats_search.append(cat)
#             for cat in material_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     material_cats_search.append(cat)
#             for cat in attribute_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     attribute_cats_search.append(cat)
#             for cat in length_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     length_cats_search.append(cat)
#             for cat in filter_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     filter_cats_search.append(cat)
#             for cat in all_cats:
#                 if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word or f'{cat}d' == word:
#                     all_cats_search.append(cat)
#
#         kind_cats_search = list(set(kind_cats_search))
#         pattern_cats_search = list(set(pattern_cats_search))
#         color_cats_search = list(set(color_cats_search))
#         style_cats_search = list(set(style_cats_search))
#         material_cats_search = list(set(material_cats_search))
#         attribute_cats_search = list(set(attribute_cats_search))
#         length_cats_search = list(set(length_cats_search))
#         all_cats_search = list(set(all_cats_search))
#         print('kind_cats_search')
#         print(kind_cats_search)
#         print('pattern_cats_search')
#         print(pattern_cats_search)
#         print('color_cats_search')
#         print(color_cats_search)
#         print('style_cats_search')
#         print(style_cats_search)
#         print('material_cats_search')
#         print(material_cats_search)
#         print('attribute_cats_search')
#         print(attribute_cats_search)
#         print('length_cats_search')
#         print(length_cats_search)
#         print('filter_cats_search')
#         print(filter_cats_search)
#         print('all_cats_search')
#         print(all_cats_search)
#         # all_cat_search_arr = np.zeros(len(all_cats))
#         # for req_tag in all_search_cats:
#         #     if req_tag in all_cats:
#         #         all_cat_search_arr[all_cats.index(req_tag)] = 1
#         #     if req_tag in ['mom', 'mamalicious', 'maternity']:
#         #         maternity = True
#
#         query_conditions = []
#         query_conds_full_text_search = []
#         query_conds_cats_kind = []
#         query_conds_cats_pattern = []
#         query_conds_cats_material = []
#         query_conds_cats_style = []
#         query_conds_cats_length = []
#         query_conds_cats_filter = []
#         query_conds_cats_all = []
#
#         for kind_cat in kind_cats_search:
#             query_conds_cats_all.append(
#                 ImagesSkinny.kind_cats.any(kind_cat)
#             )
#             query_conds_cats_kind.append(
#                 ImagesSkinny.kind_cats.any(kind_cat)
#             )
#
#         for length_cat in length_cats:
#             query_conds_cats_length.append(
#                 ImagesSkinny.length_cats.any(length_cat)
#             )
#
#         if req_sex == 'women':
#             for pattern_cat in pattern_cats_search:
#                 query_conds_cats_pattern.append(
#                     ImagesSkinny.pattern_cats.any(pattern_cat)
#                 )
#
#             for color_cat in color_cats_search:
#                 query_conds_cats_all.append(
#                     ImagesSkinny.color_cats.any(color_cat)
#                 )
#
#         for style_cat in style_cats_search:
#             query_conds_cats_style.append(
#                 ImagesSkinny.style_cats.any(style_cat)
#             )
#
#         for material_cat in material_cats_search:
#             query_conds_cats_material.append(
#                 ImagesSkinny.material_cats.any(material_cat)
#             )
#
#         for attribute_cat in attribute_cats_search:
#             query_conds_cats_all.append(
#                 ImagesSkinny.attribute_cats.any(attribute_cat)
#             )
#
#         if req_sex == 'women':
#             for length_cat in length_cats_search:
#                 query_conds_cats_length.append(
#                     ImagesSkinny.length_cats.any(length_cat)
#                 )
#
#         for filter_cat in filter_cats_search:
#             query_conds_cats_filter.append(
#                 ImagesSkinny.filter_cats.any(filter_cat)
#             )
#
#         if len(req_sex) > 2:
#             if req_sex != 'both':
#                 query_conditions.append(
#                     (ImagesSkinny.sex == req_sex)
#                 )
#
#         query_conditions.append(
#             (ImagesSkinny.shop != 'Boohoo')
#         )
#
#         query_conditions.append(
#             (ImagesSkinny.in_stock == True)
#         )
#         query_conditions.append(
#             (Images.encoding_vgg16.isnot(None))
#         )
#
#         query_conds_full_text_search.append(
#             func.lower(ImagesSkinny.name).op('@@')(func.plainto_tsquery(search_string_clean))
#         )
#
#         # ========= MAIN QUERY ===========
#         # query_results = (db.session.query(ImagesSkinny, Images).filter(
#         #     ImagesSkinny.img_hash == Images.img_hash
#         # ).filter(
#         #     and_(*query_conditions)
#         # ).limit(search_limit).all())
#
#         query_results = (db.session.query(ImagesSkinny, Images).filter(
#             ImagesSkinny.img_hash == Images.img_hash
#         ).filter(
#             and_(
#                 and_(*query_conditions),
#                 and_(*query_conds_cats_kind),
#                 or_(* query_conds_cats_length),
#                 or_(*query_conds_cats_pattern),
#                 or_(*query_conds_cats_material),
#                 or_(*query_conds_cats_style),
#                 or_(*query_conds_cats_filter)
#             )
#         ).limit(search_limit).all())
#
#         print(f'MAIN QUERY RESULT LENGTH: {len(query_results)}')
#
#         # if len(query_results) < relaxed_threshold:
#         #     # RELAXED QUERY
#         #     relaxed_query_results = (db.session.query(ImagesSkinny, Images).filter(
#         #         ImagesSkinny.img_hash == Images.img_hash
#         #     ).filter(
#         #         and_(
#         #             and_(*query_conditions_kind),
#         #             and_(*query_conditions_all)
#         #         )
#         #     ).limit(relaxed_limit).all())
#         #     query_results += relaxed_query_results
#         # print(f'NEXT RESULT LENGTH: {len(query_results)}')
#
#         if len(query_results) < relaxed_threshold:
#             # RELAXED QUERY
#             relaxed_query_results = (db.session.query(ImagesSkinny, Images).filter(
#                 ImagesSkinny.img_hash == Images.img_hash
#             ).filter(
#                 and_(
#                     # and_(*query_conditions),
#                     # and_(*query_conds_cats_kind),
#                     or_(*query_conds_full_text_search)
#                 )
#             ).limit(relaxed_limit).all())
#             query_results += relaxed_query_results
#         print(f'TOTAL RESULT LENGTH: {len(query_results)}')
#
#         # if search_color is not None:
#         #
#         #     # print('SORTING BY COLOR')
#         #     # print(search_color)
#         #     # color_list = []
#         #     # for img_table_query_result in query_results:
#         #     #     query_result = img_table_query_result[0]
#         #     #     req_color_norm_1 = np.array(search_color, dtype=int) / np.sum(np.array(search_color, dtype=int))
#         #     #
#         #     #     query_color_1_norm = np.array(query_result.color_1, dtype=int) / np.sum(
#         #     #         np.array(query_result.color_1, dtype=int))
#         #     #     query_color_2_norm = np.array(query_result.color_2, dtype=int) / np.sum(
#         #     #         np.array(query_result.color_2, dtype=int))
#         #     #     query_color_3_norm = np.array(query_result.color_3, dtype=int) / np.sum(
#         #     #         np.array(query_result.color_3, dtype=int))
#         #     #
#         #     #     # compute the chi-squared distances
#         #     #     distance_color_1 = calc_chi_distance(req_color_norm_1, query_color_1_norm)
#         #     #     distance_color_2 = calc_chi_distance(req_color_norm_1, query_color_2_norm)
#         #     #     distance_color_3 = calc_chi_distance(req_color_norm_1, query_color_3_norm)
#         #     #
#         #     #     distance_color = 10 * distance_color_1 + 3 * distance_color_2 + distance_color_3
#         #     #
#         #     #     distance_color_euc_1 = int(
#         #     #         spatial.distance.euclidean(np.array(search_color, dtype=int),
#         #     #                                    np.array(query_result.color_1, dtype=int),
#         #     #                                    w=None))
#         #     #     distance_color_euc_2 = int(
#         #     #         spatial.distance.euclidean(np.array(search_color, dtype=int),
#         #     #                                    np.array(query_result.color_2, dtype=int),
#         #     #                                    w=None))
#         #     #     distance_color_euc_3 = int(
#         #     #         spatial.distance.euclidean(np.array(search_color, dtype=int),
#         #     #                                    np.array(query_result.color_3, dtype=int),
#         #     #                                    w=None))
#         #     #
#         #     #     distance_color_euc = (1 / 500) * min([
#         #     #         distance_color_euc_1,
#         #     #         distance_color_euc_2,
#         #     #         distance_color_euc_3
#         #     #     ])
#         #     #
#         #     #     color_query_result = {
#         #     #         'img_hash': query_result.img_hash,
#         #     #         'color_dist': distance_color + distance_color_euc,
#         #     #         'prod_id': query_result.prod_id,
#         #     #         'query_result': img_table_query_result
#         #     #     }
#         #     #     color_list.append(color_query_result)
#         #     #
#         #     # sorted_color_list = sorted(color_list, key=itemgetter('color_dist'))
#         #     # top_color_list = sorted_color_list[0:80]
#         #     # result_list = []
#         #     # prod_check = set()
#         #     # print('Obtaining result data')
#         #     # for color_dict in top_color_list:
#         #     #     img_table_query_result = color_dict['query_result'][1]
#         #     #     result_prod_id = color_dict['prod_id']
#         #     #     if result_prod_id not in prod_check:
#         #     #         # prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
#         #     #         # if prod_search is not None:
#         #     #         if req_sex == 'women':
#         #     #             # prod_serial = ProductsSchema().dump(prod_search)
#         #     #             img_serial = ImagesFullSchema().dump(img_table_query_result)
#         #     #         else:
#         #     #             # prod_serial = ProductsSchema().dump(prod_search)
#         #     #             img_serial = ImagesFullSchema().dump(img_table_query_result)
#         #     #         prod_check.add(result_prod_id)
#         #     #
#         #     #         result_dict = {
#         #     #             'prod_serial': [],
#         #     #             'image_data': img_serial[0]
#         #     #         }
#         #     #         result_list.append(result_dict)
#         #
#         # else:
#         result_list = []
#         prod_check = set()
#         print('Obtaining result data')
#         for query_result in query_results:
#             img_table_query_result = query_result[1]
#             result_prod_id = img_table_query_result.prod_id
#
#             if result_prod_id not in prod_check:
#                 # prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
#                 # if prod_search is not None:
#                 # prod_serial = ProductsSchema().dump(prod_search)
#                 img_serial = ImagesFullSchema().dump(img_table_query_result)
#                 prod_check.add(result_prod_id)
#
#                 result_dict = {
#                     'prod_serial': [],
#                     'image_data': img_serial[0]
#                 }
#                 result_list.append(result_dict)
#
#         res = jsonify(res=result_list, tags=all_cats_search)
#         return res


def db_text_search_infinite_v2(data, db, Products, Images, ImagesSkinny):
    search_string = data['search_string']
    req_sex = data['sex']
    prev_prod_ids = data['prev_prod_ids']
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
