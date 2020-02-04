from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ProductSchemaV2, ImageSchemaV2, ImagesFullWomenASchema, ProductsWomenASchema
import scipy.spatial as spatial
import numpy as np
from operator import itemgetter
import json
# from color_text import color_check
from flask import jsonify
# from data import cats
import data.cats as cats


def search_similar_images(request, db, ImagesV2, ImagesV2Skinny, ProductsV2):
    data = request.get_json(force=True)
    data = json.loads(data)
    req_img_hash = data['img_hash']
    req_tags_positive = data['tags_positive']
    req_tags_negative = data['tags_negative']
    req_color_1 = data['color_1']
    req_sex = data['sex']
    max_price = int(data['max_price'])
    req_brands = data['brands']

    req_image_data = ImagesV2.query.filter_by(img_hash=req_img_hash).first()

    result_limit = 500

    print('RGB 1: ', str(req_color_1))
    print(f'Positive tags: {req_tags_positive}')
    print(f'Negative tags: {req_tags_negative}')

    if req_tags_positive is None:
        req_tags_positive = req_image_data.all_cats

    print(f'Updated Positive tags: {req_tags_positive}')

    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    style_cats = tag_list.style_cats
    filter_cats = tag_list.filter_cats
    length_cats = tag_list.length_cats
    color_pattern_cats = tag_list.color_pattern_cats
    material_cats = tag_list.material_cats
    kind_search_cats = [req_tag for req_tag in req_tags_positive if req_tag in kind_cats]
    style_search_cats = [req_tag for req_tag in req_tags_positive if req_tag in style_cats]
    length_search_cats = [req_tag for req_tag in req_tags_positive if req_tag in length_cats]
    color_pattern_search_cats = [req_tag for req_tag in req_tags_positive if req_tag in color_pattern_cats]
    filter_search_cats = [req_tag for req_tag in req_tags_positive if req_tag in filter_cats]
    material_search_cats = [req_tag for req_tag in req_tags_positive if req_tag in material_cats]

    search_string_clean = ' '.join(req_tags_positive)

    print(f'KIND CATS: {kind_search_cats}')
    print(f'STYLE CATS: {style_search_cats}')
    print(f'LENGTH CATS: {length_search_cats}')
    print(f'COLOR PATTERN CATS: {color_pattern_search_cats}')
    print(f'FILTER CATS: {filter_search_cats}')
    print(f'MATERIAL CATS: {material_search_cats}')

    print('Assembling db query conditions')
    conditions_base = []
    conditions_kind_cats = []
    conditions_style_cats = []
    conditions_length_cats = []
    conditions_color_pattern_cats = []
    conditions_filter_cats = []
    conditions_all_cats = []
    conditions_material = []
    conditions_brand = []
    query_conditions_all = []

    maternity = False
    for tag in req_tags_positive:
        conditions_all_cats.append(
            (ImagesV2Skinny.all_cats.any(tag))
        )
        if tag in ['mom', 'mamalicious', 'maternity']:
            maternity = True

    # if maternity == False:
    #     print('NO MATERNITY')
    #     conditions_base.append(
    #         (~ImagesV2Skinny.all_cats.any('maternity'))
    #     )
    #     conditions_base.append(
    #         (~ImagesV2Skinny.filter_cats.any('maternity'))
    #     )
    #     conditions_base.append(
    #         (~ImagesV2Skinny.name.ilike('%{0}%'.format('maternity')))
    #     )
    #     conditions_base.append(
    #         (~ImagesV2Skinny.all_cats.any('mamalicious'))
    #     )
    #     conditions_base.append(
    #         (~ImagesV2Skinny.filter_cats.any('mamalicious'))
    #     )
    #     conditions_base.append(
    #         (~ImagesV2Skinny.all_cats.any('mom'))
    #     )

    for kind_search_cat in kind_search_cats:
        conditions_kind_cats.append(
            (ImagesV2Skinny.all_cats.any(kind_search_cat))
        )

    for filter_search_cat in filter_search_cats:
        conditions_filter_cats.append(
            (ImagesV2Skinny.filter_cats.any(filter_search_cat))
        )

    for style_search_cat in style_search_cats:
        conditions_style_cats.append(
            (ImagesV2Skinny.style_cats.any(style_search_cat))
        )

    for length_search_cat in length_search_cats:
        conditions_length_cats.append(
            (ImagesV2Skinny.all_cats.any(length_search_cat))
        )

    for color_pattern_search_cat in color_pattern_search_cats:
        conditions_color_pattern_cats.append(
            (ImagesV2Skinny.color_pattern_cats.any(color_pattern_search_cat))
        )

    for material_search_cat in material_search_cats:
        conditions_material.append(
            (ImagesV2Skinny.material_cats.any(material_search_cat))
        )

    for tag in req_tags_negative:
        print(f'negative tag: {tag}')
        conditions_base.append(
            (~ImagesV2Skinny.all_cats.any(tag))
        )

    if len(req_sex) > 2:
        conditions_base.append(
            (ImagesV2Skinny.sex == req_sex)
        )

    if len(req_brands) > 0:
        for req_brand in req_brands:
            conditions_brand.append(
                (ImagesV2Skinny.brand == req_brand)
            )
            conditions_brand.append(
                (ImagesV2Skinny.brand.ilike('%{0}%'.format(req_brand)))
            )
        print('filtering for brands')
        print(req_brands)

    if max_price < 1000000:
        conditions_base.append(
            or_((ImagesV2Skinny.price < max_price),
                and_((ImagesV2Skinny.sale == True), (ImagesV2Skinny.saleprice < max_price)))
        )
    conditions_base.append(
        (ImagesV2Skinny.in_stock == True)
    )
    conditions_base.append(
        (ImagesV2.encoding_vgg16 != None)
    )
    query_conditions_all.append(
        (func.lower(ImagesV2Skinny.name).op('%%')(search_string_clean))
    )

    # ====== MAIN QUERY ======
    img_table_query_results = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
        ImagesV2Skinny.img_hash == ImagesV2.img_hash
    ).filter(
        and_(
            and_(*conditions_base),
            and_(*conditions_kind_cats),
            and_(*conditions_length_cats),
            or_(*conditions_style_cats),
            or_(*conditions_color_pattern_cats),
            or_(*conditions_material),
            and_(*conditions_filter_cats),
            or_(*conditions_brand)
        )
    ).limit(result_limit).all())

    print(f'RESULT LENGTH: {len(img_table_query_results)}')

    if len(img_table_query_results) < 50:
        print('ADDING RELAXED RESULTS')
        query_results_relaxed = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
            ImagesV2Skinny.img_hash == ImagesV2.img_hash
        ).filter(
            and_(
                and_(*conditions_base),
                and_(*conditions_kind_cats),
                and_(*conditions_length_cats),
                or_(*conditions_style_cats),
                and_(*conditions_filter_cats),
                or_(*conditions_brand)
            )
        ).limit(50 - len(img_table_query_results)).all())

        print(f'{len(query_results_relaxed)} RELAXED RESULTS ADDED')

        img_table_query_results += query_results_relaxed

    if len(img_table_query_results) < 50:
        print('ADDING EVEN MORE RELAXED RESULTS')
        query_results_relaxed_2 = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
            ImagesV2Skinny.img_hash == ImagesV2.img_hash
        ).filter(
            and_(
                and_(*conditions_base),
                or_(*conditions_kind_cats),
                or_(*query_conditions_all),
                or_(*conditions_filter_cats),
            )
        ).limit(50 - len(img_table_query_results)).all())

        print(f'{len(query_results_relaxed_2)} MORE RELAXED RESULTS ADDED')

        img_table_query_results += query_results_relaxed_2

    if len(img_table_query_results) < 30:
        print('ADDING EVEN MORE RELAXED RESULTS')
        query_results_relaxed_3 = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
            ImagesV2Skinny.img_hash == ImagesV2.img_hash
        ).filter(
            and_(
                and_(*conditions_base),
                or_(*conditions_all_cats)
            )
        ).limit(30).all())

        print(f'{len(query_results_relaxed_3)} MORE RELAXED RESULTS ADDED')

        img_table_query_results += query_results_relaxed_3

    req_encoding_crop = req_image_data.encoding_crop
    req_encoding_vgg16 = req_image_data.encoding_vgg16

    # Start with main RBG color distances to reduce the amount of the rest of the distances to calc
    print(f'TOTAL RESULT LENGTH: {len(img_table_query_results)}')
    color_list = []
    for img_table_query_result in img_table_query_results:
        query_result = img_table_query_result[1]
        try:
            image_prod_name = query_result.name
            vgg_16_len = len(query_result.encoding_vgg16)
        except:
            image_prod_name = None
            vgg_16_len = 0
        if image_prod_name is not None and vgg_16_len == 4096:
            image_prod_name_arr = image_prod_name.lower().strip('*\'[]\*').split(' ')

            neg_tag_check = False
            for neg_tag in req_tags_negative:
                neg_tag_check = neg_tag in image_prod_name_arr

            if neg_tag_check is False:
                req_color_norm_1 = np.array(req_color_1, dtype=int) / np.sum(np.array(req_color_1, dtype=int))
                # req_color_norm_2 = np.array(req_color_2, dtype=int) / np.sum(np.array(req_color_2, dtype=int))
                query_color_1_norm = np.array(query_result.color_1, dtype=int) / np.sum(
                    np.array(query_result.color_1, dtype=int))
                query_color_2_norm = np.array(query_result.color_2, dtype=int) / np.sum(
                    np.array(query_result.color_2, dtype=int))
                # query_color_3_norm = np.array(query_result.color_3, dtype=int) / np.sum(
                #     np.array(query_result.color_3, dtype=int))

                # compute the chi-squared distances
                distance_color_1 = calc_chi_distance(req_color_norm_1, query_color_1_norm)
                distance_color_2 = calc_chi_distance(req_color_norm_1, query_color_2_norm)
                # distance_color_3 = calc_chi_distance(req_color_norm_1, query_color_3_norm)
                # distance_color_1_2 = calc_chi_distance(req_color_norm_2, query_color_1_norm)
                # distance_color_2_2 = calc_chi_distance(req_color_norm_2, query_color_2_norm)
                # distance_color_3_2 = calc_chi_distance(req_color_norm_2, query_color_3_norm)
                # distance_color = 2 * min([
                #     distance_color_1,
                #     distance_color_2,
                #     # distance_color_3
                # ]) + min([
                #     distance_color_1_2,
                #     distance_color_2_2,
                #     # distance_color_3_2
                # ])
                distance_color = 2 * (distance_color_1 + distance_color_2)
                # print('Chi distance: ', str(distance_color))

                distance_color_euc_1 = int(
                    spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                               np.array(query_result.color_1, dtype=int),
                                               w=None))
                distance_color_euc_2 = int(
                    spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                               np.array(query_result.color_2, dtype=int),
                                               w=None))
                # distance_color_euc_3 = int(
                #     spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                #                                np.array(query_result.color_3, dtype=int),
                #                                w=None))

                # distance_color_euc_1_2 = int(
                #     spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                #                                np.array(query_result.color_1, dtype=int),
                #                                w=None))
                # distance_color_euc_2_2 = int(
                #     spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                #                                np.array(query_result.color_2, dtype=int),
                #                                w=None))
                # distance_color_euc_3_2 = int(
                #     spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                #                                np.array(query_result.color_3, dtype=int),
                #                                w=None))

                # distance_color_euc = (1 / 500) * (2 * min([
                #     distance_color_euc_1,
                #     distance_color_euc_2,
                #     # distance_color_euc_3
                # ]) + min([
                #     distance_color_euc_1_2,
                #     distance_color_euc_2_2,
                #     # distance_color_euc_3_2
                # ]))
                distance_color_euc = (1 / 500) * (2 * (distance_color_euc_1 + distance_color_euc_2))
                # print('Euclidean distance: ', str(distance_color_euc))
                color_query_result = {
                    'query_result': query_result,
                    'img_hash': query_result.img_hash,
                    'prod_id': query_result.prod_id,
                    'color_dist': distance_color_euc + distance_color
                }
                color_list.append(color_query_result)

    sorted_color_list = sorted(color_list, key=itemgetter('color_dist'))
    top_color_list = sorted_color_list[0:int(result_limit * 0.7)]

    # CALCULATE ENCODING DISTANCES
    encoding_arrays = []
    for query_result in top_color_list:
        encoding_arrays.append(query_result['query_result'].encoding_vgg16)
    encoding_matrix = np.asarray(encoding_arrays)

    dist_encoding_arr = np.linalg.norm(encoding_matrix - req_encoding_vgg16, axis=1)
    closest_n_enc_ind = dist_encoding_arr.argsort()[:int(result_limit * 0.5)]
    closest_n_enc_results = [top_color_list[x] for x in closest_n_enc_ind]
    print(f'Closest encodings calculated, length: {len(closest_n_enc_results)}')

    # Calculate cropped encoding vector distances
    encoding_crop_list = []
    for encoding_result in closest_n_enc_results:
        query_result = encoding_result['query_result']
        encoding_crop_dist = int(
            spatial.distance.euclidean(np.array(req_encoding_crop, dtype=int),
                                       np.array(query_result.encoding_crop, dtype=int),
                                       w=None))
        encoding_result = {
            'query_result': query_result,
            'img_hash': query_result.img_hash,
            'prod_id': query_result.prod_id,
            'color_dist': encoding_result['color_dist'],
            'encoding_crop_dist': encoding_crop_dist
        }
        encoding_crop_list.append(encoding_result)

    # Make sure we return the original request image back on top
    if not any(d['img_hash'] == req_img_hash for d in encoding_crop_list):
        print('Product not in list, need to add')
        encoding_crop_list.insert(0, {
            'img_hash': req_img_hash,
            'prod_id': req_image_data.prod_id,
            'query_result': req_image_data,
            'encoding_crop_dist': -1000,
            'color_dist': -1000
        })
    else:
        print('Product already in list, need to make sure its on top')
        request_prod = next(item for item in encoding_crop_list if item['img_hash'] == req_img_hash)
        request_prod['color_dist'] = -1000
        request_prod['encoding_crop_dist'] = -1000

    sorted_encoding_crop_list = sorted(encoding_crop_list, key=itemgetter('encoding_crop_dist'))
    top_encoding_crop_list = sorted_encoding_crop_list[0:int(result_limit * 0.3)]
    print(f'Crop encoding distances, length: {len(top_encoding_crop_list)}')

    top_encoding_sqcrop_list = sorted(top_encoding_crop_list, key=itemgetter('color_dist'))
    top_encoding_sqcrop_list = top_encoding_sqcrop_list[0:50]

    # Serialize the results and return as array
    result_list = []
    prod_check = set()
    print('Obtaining result data')
    for obj in top_encoding_sqcrop_list:
        result_prod_id = obj['prod_id']
        prod_search = db.session.query(ProductsV2).filter(ProductsV2.prod_id == result_prod_id).first()
        prod_hash = prod_search.prod_id
        if prod_hash not in prod_check:
            prod_serial = ProductSchemaV2().dump(prod_search)
            prod_check.add(prod_hash)
            img_serial = ImageSchemaV2().dump(obj['query_result'])
            result_dict = {
                'prod_serial': prod_serial[0],
                'image_data': img_serial[0]
            }
            result_list.append(result_dict)

    return result_list


def calc_chi_distance(hist_1, hist_2, eps=1e-10):
    # compute the chi-squared distance
    distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_1, hist_2)])

    return distance


def calc_cross_entropy(vector_1, vector_2):
    dist = np.sum(vector_1 * np.log(vector_2) + (1 - vector_1) * np.log(1 - vector_2))

    return dist


#######################################################################################################################
#######################################################################################################################


def search_from_upload(request, db, ImagesV2, ImagesV2Skinny, ProductsV2):
    data = request.get_json(force=True)
    data = json.loads(data)
    print('Request received')
    req_tags = data['tags']
    req_sex = data['sex']
    # req_shop_excl = data['no_shop']
    req_color_1 = data['color_1']
    # req_color_2 = data['color_2']
    req_encoding = data['encoding_rcnn']
    req_vgg16_encoding = data['vgg16_encoding']

    result_limit = 1000

    req_vgg16_encoding_arr = np.asarray(req_vgg16_encoding)
    req_encoding_arr = np.asarray(req_encoding)

    print(f'Req tags: {req_tags}')

    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    style_cats = tag_list.style_cats
    filter_cats = tag_list.filter_cats
    length_cats = tag_list.length_cats
    color_pattern_cats = tag_list.color_pattern_cats
    kind_search_cats = [req_tag for req_tag in req_tags if req_tag in kind_cats]
    style_search_cats = [req_tag for req_tag in req_tags if req_tag in style_cats]
    length_search_cats = [req_tag for req_tag in req_tags if req_tag in length_cats]
    color_pattern_search_cats = [req_tag for req_tag in req_tags if req_tag in color_pattern_cats]
    filter_search_cats = [req_tag for req_tag in req_tags if req_tag in filter_cats]

    print(f'KIND CATS: {kind_search_cats}')
    print(f'STYLE CATS: {style_search_cats}')
    print(f'LENGTH CATS: {length_search_cats}')
    print(f'COLOR PATTERN CATS: {color_pattern_search_cats}')

    print('Assembling db query conditions')
    conditions_base = []
    conditions_kind_cats = []
    conditions_style_cats = []
    conditions_length_cats = []
    conditions_color_pattern_cats = []
    conditions_filter_cats = []
    conditions_all_cats = []

    maternity = False
    for tag in req_tags:
        conditions_all_cats.append(
            ImagesV2Skinny.all_cats.any(tag)
        )
        if tag in ['mom', 'mamalicious', 'maternity']:
            maternity = True

    for kind_search_cat in kind_search_cats:
        conditions_kind_cats.append(
            ImagesV2Skinny.kind_cats.any(kind_search_cat)
        )

    if maternity == False:
        print('NO MATERNITY')
        conditions_base.append(
            (~ImagesV2Skinny.all_cats.any('maternity'))
        )
        conditions_base.append(
            (~ImagesV2Skinny.filter_cats.any('maternity'))
        )
        conditions_base.append(
            (~ImagesV2Skinny.name.ilike('%{0}%'.format('maternity')))
        )
        conditions_base.append(
            (~ImagesV2Skinny.all_cats.any('mamalicious'))
        )
        conditions_base.append(
            (~ImagesV2Skinny.filter_cats.any('mamalicious'))
        )
        conditions_base.append(
            (~ImagesV2Skinny.all_cats.any('mom'))
        )

    for filter_search_cat in filter_search_cats:
        conditions_filter_cats.append(
            ImagesV2Skinny.filter_cats.any(filter_search_cat)
        )

    for style_search_cat in style_search_cats:
        conditions_style_cats.append(
            ImagesV2Skinny.style_cats.any(style_search_cat)
        )

    for length_search_cat in length_search_cats:
        conditions_length_cats.append(
            ImagesV2Skinny.all_cats.any(length_search_cat)
        )

    for color_pattern_search_cat in color_pattern_search_cats:
        conditions_color_pattern_cats.append(
            ImagesV2Skinny.color_pattern_cats.any(color_pattern_search_cat)
        )

    if len(req_sex) > 2:
        conditions_base.append(
            (ImagesV2Skinny.sex == req_sex)
        )

    conditions_base.append(
        (ImagesV2Skinny.in_stock == True)
    )
    conditions_base.append(
        (ImagesV2.encoding_vgg16 != None)
    )

    # ====== MAIN QUERY ======
    img_table_query_results = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
        ImagesV2Skinny.img_hash == ImagesV2.img_hash
    ).filter(
        and_(
            and_(*conditions_base),
            and_(*conditions_all_cats)
        )
    ).limit(result_limit).all())

    print(f'RESULT LENGTH: {len(img_table_query_results)}')

    if len(img_table_query_results) < result_limit:
        print('ADDING RELAXED RESULTS')
        query_results_relaxed = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
            ImagesV2Skinny.img_hash == ImagesV2.img_hash
        ).filter(
            and_(
                and_(*conditions_base),
                and_(*conditions_kind_cats),
                and_(*conditions_length_cats),
                or_(*conditions_style_cats),
                or_(*conditions_color_pattern_cats),
                and_(*conditions_filter_cats)
            )
        ).limit(result_limit - len(img_table_query_results)).all())

        print(f'{len(query_results_relaxed)} RELAXED RESULTS ADDED')

        img_table_query_results += query_results_relaxed

    if len(img_table_query_results) < 200:
        print('ADDING EVEN MORE RELAXED RESULTS')
        query_results_relaxed_2 = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
            ImagesV2Skinny.img_hash == ImagesV2.img_hash
        ).filter(
            and_(
                and_(*conditions_base),
                and_(*conditions_kind_cats),
                and_(*conditions_length_cats),
                or_(*conditions_style_cats),
                and_(*conditions_filter_cats)
            )
        ).limit(200).all())

        print(f'{len(query_results_relaxed_2)} MORE RELAXED RESULTS ADDED')

        img_table_query_results += query_results_relaxed_2

    if len(img_table_query_results) < 200:
        print('ADDING EVEN EVEN MORE RELAXED RESULTS')
        query_results_relaxed_2 = (db.session.query(ImagesV2Skinny, ImagesV2).filter(
            ImagesV2Skinny.img_hash == ImagesV2.img_hash
        ).filter(
            and_(
                and_(*conditions_base),
                or_(*conditions_kind_cats),
                and_(*conditions_length_cats),
                or_(*conditions_style_cats),
                and_(*conditions_filter_cats)
            )
        ).limit(100).all())

        print(f'{len(query_results_relaxed_2)} MORE RELAXED RESULTS ADDED')

        img_table_query_results += query_results_relaxed_2


    if len(img_table_query_results) == 0:
        return 'No results'
    else:
        print('Query results obtained')

        # CALCULATE COLOR DISTANCE
        color_list = []
        for img_table_query_result in img_table_query_results:
            query_result = img_table_query_result[1]
            req_color_norm_1 = np.array(req_color_1, dtype=int) / np.sum(np.array(req_color_1, dtype=int))
            # req_color_norm_2 = np.array(req_color_2, dtype=int) / np.sum(np.array(req_color_2, dtype=int))
            query_color_1_norm = np.array(query_result.color_1, dtype=int) / np.sum(
                np.array(query_result.color_1, dtype=int))
            query_color_2_norm = np.array(query_result.color_2, dtype=int) / np.sum(
                np.array(query_result.color_2, dtype=int))
            # query_color_3_norm = np.array(closest_n_result.color_3, dtype=int) / np.sum(
            #     np.array(closest_n_result.color_3, dtype=int))

            # compute the chi-squared distances
            distance_color_1 = calc_chi_distance(req_color_norm_1, query_color_1_norm)
            distance_color_2 = calc_chi_distance(req_color_norm_1, query_color_2_norm)
            # distance_color_3 = calc_chi_distance(req_color_norm_1, query_color_3_norm)
            # distance_color_1_2 = calc_chi_distance(req_color_norm_2, query_color_1_norm)
            # distance_color_2_2 = calc_chi_distance(req_color_norm_2, query_color_2_norm)
            # distance_color_3_2 = calc_chi_distance(req_color_norm_2, query_color_3_norm)
            # distance_color = 2 * min([
            #     distance_color_1,
            #     distance_color_2,
            #     # distance_color_3
            # ]) + min([
            #     distance_color_1_2,
            #     distance_color_2_2,
            #     # distance_color_3_2
            # ])
            distance_color = 2 * (distance_color_1 + distance_color_2)
            # print('Chi distance: ', str(distance_color))

            distance_color_euc_1 = int(
                spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                           np.array(query_result.color_1, dtype=int),
                                           w=None))
            distance_color_euc_2 = int(
                spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                           np.array(query_result.color_2, dtype=int),
                                           w=None))
            # distance_color_euc_3 = int(
            #     spatial.distance.euclidean(np.array(req_color_1, dtype=int),
            #                                np.array(closest_n_result.color_3, dtype=int),
            #                                w=None))

            # distance_color_euc_1_2 = int(
            #     spatial.distance.euclidean(np.array(req_color_2, dtype=int),
            #                                np.array(closest_n_result.color_1, dtype=int),
            #                                w=None))
            # distance_color_euc_2_2 = int(
            #     spatial.distance.euclidean(np.array(req_color_2, dtype=int),
            #                                np.array(closest_n_result.color_2, dtype=int),
            #                                w=None))
            # distance_color_euc_3_2 = int(
            #     spatial.distance.euclidean(np.array(req_color_2, dtype=int),
            #                                np.array(closest_n_result.color_3, dtype=int),
            #                                w=None))

            # distance_color_euc = (1 / 500) * (2 * min([
            #     distance_color_euc_1,
            #     distance_color_euc_2,
            #     # distance_color_euc_3
            # ]) + min([
            #     distance_color_euc_1_2,
            #     distance_color_euc_2_2,
            #     # distance_color_euc_3_2
            # ]))
            distance_color_euc = (1 / 500) * (2 * (distance_color_euc_1 + distance_color_euc_2))
            # print('Euclidean distance: ', str(distance_color_euc))
            color_query_result = {
                'all_arr': query_result.all_arr,
                'encoding_crop': query_result.encoding_crop,
                'encoding_vgg16': query_result.encoding_vgg16,
                'img_hash': query_result.img_hash,
                'color_dist': distance_color + distance_color_euc
            }
            color_list.append(color_query_result)

        sorted_color_list = sorted(color_list, key=itemgetter('color_dist'))
        top_color_list = sorted_color_list[0:500]
        print('Closest colors calculated')

        # # CALCULATE TAG SIMILARITY
        # all_cat_arrays = []
        # for query_result in top_color_list:
        #     all_cat_arrays.append(query_result['all_arr'])
        # all_cat_matrix = np.asarray(all_cat_arrays)
        # print(f'all_cat_matrix.shape : {all_cat_matrix.shape}')
        # print(f'all_cat_search_arr.shape : {all_cat_search_arr.shape}')
        # similarity_matrix = np.sum(all_cat_matrix * all_cat_search_arr, axis=1)
        # closest_n_indices = similarity_matrix.argsort()[-1500:][::-1]
        # closest_n_results = [top_color_list[x] for x in closest_n_indices]
        # print('Closest all cats calculated')

        # Calculate VGG16 encoding distances
        vgg16_arrays = []
        for query_result in top_color_list:
            vgg16_arrays.append(query_result['encoding_vgg16'])
        vgg16_matrix = np.asarray(vgg16_arrays)
        print(f'vgg16_matrix.shape : {vgg16_matrix.shape}')
        print(f'req_vgg16_encoding_arr.shape : {req_vgg16_encoding_arr.shape}')
        dist_vgg16_arr = np.linalg.norm(vgg16_matrix - req_vgg16_encoding_arr, axis=1)
        closest_n_vgg16_ind = dist_vgg16_arr.argsort()[:300]
        closest_n_vgg16_results = [top_color_list[x] for x in closest_n_vgg16_ind]

        # CALCULATE ENCODING DISTANCES
        encoding_arrays = []
        for query_result in closest_n_vgg16_results:
            encoding_arrays.append(query_result['encoding_crop'])
        encoding_matrix = np.asarray(encoding_arrays)

        dist_encoding_arr = np.linalg.norm(encoding_matrix - req_encoding_arr, axis=1)
        closest_n_enc_ind = dist_encoding_arr.argsort()[:200]
        closest_n_enc_results = [closest_n_vgg16_results[x] for x in closest_n_enc_ind]
        print('Closest encodings calculated')

        final_sorted_color_list = sorted(closest_n_enc_results, key=itemgetter('color_dist'))
        final_top_color_list = final_sorted_color_list[0:50]

        result_list = []
        prod_check = set()
        for closest_n_color_result in final_top_color_list:
            result_img_hash = closest_n_color_result['img_hash']

            img_search = db.session.query(
                ImagesV2.name,
                ImagesV2.img_hash,
                ImagesV2.prod_id,
                ImagesV2.color_1,
                ImagesV2.color_1_hex,
                ImagesV2.color_2,
                ImagesV2.color_2_hex,
                ImagesV2.color_3,
                ImagesV2.color_3_hex,
                ImagesV2.encoding_crop,
                ImagesV2.encoding_vgg16,
                ImagesV2.all_arr,
                ImagesV2.all_cats,
                ImagesV2.size_stock,
                ImagesV2.img_url,
                ImagesV2.price,
                ImagesV2.sale,
                ImagesV2.saleprice,
                ImagesV2.in_stock,
                ImagesV2.shop,
                ImagesV2.prod_url
            ).filter(ImagesV2.img_hash == result_img_hash).first()
            prod_hash = img_search.prod_id
            if prod_hash not in prod_check:
                prod_check.add(prod_hash)
                img_serial = ImageSchemaV2().dump(img_search)
                prod_search = db.session.query(
                    ProductsV2.prod_id,
                    ProductsV2.name,
                    ProductsV2.prod_url,
                    ProductsV2.brand,
                    ProductsV2.category,
                    ProductsV2.color_string,
                    ProductsV2.currency,
                    ProductsV2.date,
                    ProductsV2.description,
                    ProductsV2.image_hash,
                    ProductsV2.image_urls,
                    ProductsV2.price,
                    ProductsV2.sale,
                    ProductsV2.saleprice,
                    ProductsV2.sex,
                    ProductsV2.shop,
                    ProductsV2.size_stock,
                ).filter(ProductsV2.prod_id == prod_hash).first()
                prod_serial = ProductSchemaV2().dump(prod_search)

                result_dict = {
                    'prod_serial': prod_serial[0],
                    'image_data': img_serial[0]
                }
                result_list.append(result_dict)
        print('Results obtained from DB')

        return result_list


#######################################################################################################################
#######################################################################################################################


def db_text_search(request, db, Products, Images):
    search_string = request.args.get('search_string')
    print('search string: ' + search_string)
    search_string.replace('+', ' ')
    req_sex = request.args.get('sex')

    string_list = search_string.strip().lower().split()
    linking_words = ['with', 'on', 'under', 'over', 'at', 'like', 'in', 'for', 'as', 'after', 'by', 'and']
    string_list_clean = [e for e in string_list if e not in linking_words]
    print('Cleaned string list', str(string_list_clean))
    search_string_clean = ' '.join(string_list_clean)

    maternity = False
    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    pattern_cats = tag_list.pattern_cats
    color_cats = tag_list.color_cats
    style_cats = tag_list.style_cats
    material_cats = tag_list.material_cats
    attribute_cats = tag_list.attribute_cats
    length_cats = tag_list.length_cats
    filter_cats = tag_list.filter_cats
    all_cats = tag_list.all_cats
    # kind_search_cats = [req_tag for req_tag in string_list_clean if req_tag in kind_cats or f'{req_tag}s' in kind_cats or f'{req_tag}es' in kind_cats or f'{req_tag}ed' in kind_cats]
    # pattern_search_cats = [req_tag for req_tag in string_list_clean if req_tag in pattern_cats or f'{req_tag}s' in pattern_cats or f'{req_tag}es' in pattern_cats or f'{req_tag}ed' in pattern_cats]
    # color_search_cats = [req_tag for req_tag in string_list_clean if req_tag in color_cats or f'{req_tag}s' in color_cats or f'{req_tag}es' in color_cats or f'{req_tag}ed' in color_cats]
    # all_search_cats = [req_tag for req_tag in string_list_clean if req_tag in all_cats or f'{req_tag}s' in all_cats or f'{req_tag}es' in all_cats or f'{req_tag}ed' in all_cats]
    kind_cats_search = []
    pattern_cats_search = []
    color_cats_search = []
    style_cats_search = []
    material_cats_search = []
    attribute_cats_search = []
    length_cats_search = []
    filter_cats_search = []
    all_cats_search = []

    for word in string_list_clean:
        for cat in kind_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                kind_cats_search.append(cat)
        for cat in pattern_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                pattern_cats_search.append(cat)
        for cat in color_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                color_cats_search.append(cat)
        for cat in style_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                style_cats_search.append(cat)
        for cat in material_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                material_cats_search.append(cat)
        for cat in attribute_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                attribute_cats_search.append(cat)
        for cat in length_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                length_cats_search.append(cat)
        for cat in filter_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                filter_cats_search.append(cat)
        for cat in all_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                all_cats_search.append(cat)

    print('kind_cats_search')
    print(kind_cats_search)
    print('pattern_cats_search')
    print(pattern_cats_search)
    print('color_cats_search')
    print(color_cats_search)
    print('style_cats_search')
    print(style_cats_search)
    print('material_cats_search')
    print(material_cats_search)
    print('attribute_cats_search')
    print(attribute_cats_search)
    print('length_cats_search')
    print(length_cats_search)
    print('filter_cats_search')
    print(filter_cats_search)
    print('all_cats_search')
    print(all_cats_search)
    # all_cat_search_arr = np.zeros(len(all_cats))
    # for req_tag in all_search_cats:
    #     if req_tag in all_cats:
    #         all_cat_search_arr[all_cats.index(req_tag)] = 1
    #     if req_tag in ['mom', 'mamalicious', 'maternity']:
    #         maternity = True

    query_conditions = []
    query_conditions_all = []
    for kind_cat in kind_cats_search:
        query_conditions.append(
            Images.kind_cats.any(kind_cat)
        )

    for pattern_cat in pattern_cats_search:
        query_conditions.append(
            Images.pattern_cats.any(pattern_cat)
        )

    for color_cat in color_cats_search:
        query_conditions.append(
            Images.color_cats.any(color_cat)
        )

    for style_cat in style_cats_search:
        query_conditions.append(
            Images.style_cats.any(style_cat)
        )

    for material_cat in material_cats_search:
        query_conditions.append(
            Images.material_cats.any(material_cat)
        )

    for attribute_cat in attribute_cats_search:
        query_conditions.append(
            Images.attribute_cats.any(attribute_cat)
        )

    for length_cat in length_cats_search:
        query_conditions.append(
            Images.length_cats.any(length_cat)
        )

    for filter_cat in filter_cats_search:
        query_conditions.append(
            Images.filter_cats.any(filter_cat)
        )

    if len(req_sex) > 2:
        query_conditions.append(
            (Images.sex == req_sex)
        )
    query_conditions.append(
        (Images.shop != 'Boohoo')
    )
    # for all_search_cat in all_cats_search:
    #     query_conditions_all.append(
    #         Images.all_cats.any(all_search_cat)
    #     )
    # if maternity == False:
    #     query_conditions.append(
    #         (~ImagesV2.all_cats.any('maternity'))
    #     )
    #     query_conditions.append(
    #         (~ImagesV2.all_cats.any('mamalicious'))
    #     )
    #     query_conditions.append(
    #         (~ImagesV2.all_cats.any('mom'))
    #     )

    query_conditions.append(
        (Images.in_stock == True)
    )
    query_conditions.append(
        (Images.encoding_vgg16 != None)
    )

    query_conditions_all.append(
        func.lower(Images.name).op('%%')(search_string_clean)
    )

    # query = db.session.query(Images).filter(
    #     and_(and_(*query_conditions), or_(*query_conditions_all))
    # )

    query = db.session.query(Images).filter(
        and_(*query_conditions)
    )

    query_results = query.order_by(func.random()).limit(100).all()

    print(f'RESULT LENGTH: {len(query_results)}')

    if len(query_results) < 50:
        relaxed_query = db.session.query(Images).filter(
            and_(or_(*query_conditions), or_(*query_conditions_all))
        )
        relaxed_query_results = relaxed_query.order_by(func.random()).limit(50).all()
        query_results += relaxed_query_results

    result_list = []
    prod_check = set()
    print('Obtaining result data')
    for img_table_query_result in query_results:
        # obj = img_table_query_result[1]
        result_prod_id = img_table_query_result.prod_id

        # prod_hash = prod_search.prod_id
        if result_prod_id not in prod_check:
            prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
            if prod_search is not None:
                if req_sex == 'women':
                    prod_serial = ProductsWomenASchema().dump(prod_search)
                    img_serial = ImagesFullWomenASchema().dump(img_table_query_result)

                prod_check.add(result_prod_id)

                result_dict = {
                    'prod_serial': prod_serial[0],
                    'image_data': img_serial[0]
                }
                result_list.append(result_dict)

    res = jsonify(res=result_list, tags=all_cats_search)
    return res


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
        prod_serial = ProductSchemaV2().dump(prod_search)

        result_dict = {
            'count': result_len,
            'prod_serial': prod_serial[0]
        }
        result_list.append(result_dict)

    return result_list

