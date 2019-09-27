from sqlalchemy import func, any_, and_
from marshmallow_schema import ProductSchemaV2, ImageSchema, ProductSchema, ImageSchemaV2
import scipy.spatial as spatial
import numpy as np
from operator import itemgetter
import json
from color_text import color_check
from flask import jsonify
# from data import cats
import data.cats as cats


def search_similar_images(request, db, Images, Products):
    req_img_hash = request.args.get('img_hash')
    req_tags_positive = request.args.get('tags_positive').strip('\'[]').split(',')
    req_tags_negative = request.args.get('tags_negative').strip('\'[]').split(',')
    req_color_1 = request.args.get('color_1').strip('\'[]').split(',')  # RGB color array
    req_color_2 = request.args.get('color_2').strip('\'[]').split(',')  # RGB color array
    req_sex = request.args.get('sex')
    req_image_data = Images.query.filter_by(img_hash=req_img_hash).first()
    req_shop_excl = request.args.get('no_shop')
    print('RGB 1: ', str(req_color_1))
    print('RGB 2: ', str(req_color_2))
    # Assemble DB query conditions in array from tags
    print('Assembling db query conditions')
    conditions = []
    for tag in req_tags_positive:
        conditions.append(
            Images.img_cats_ai_txt.any(tag) | Images.img_cats_sc_txt.any(tag) | Images.name.ilike('%{0}%'.format(tag))
        )
    for tag in req_tags_negative:
        conditions.append(
            (any_(Images.img_cats_sc_txt) != tag)
        )
    if len(req_sex) > 2:
        conditions.append(
            (Images.sex == req_sex)
        )
    if len(req_shop_excl) > 0:
        conditions.append(
            (Images.shop != any_(req_shop_excl))
        )
    # Use those conditions as argument for a filter function
    print('Querying database')
    query = db.session.query(Images).filter(
        and_(*conditions)
    )
    query_results = query.order_by(func.random()).limit(2000).all()

    if len(query_results) == 0:
        return 'no results'
    else:
        req_color_512 = req_image_data.color_512
        req_encoding_nocrop = req_image_data.encoding_nocrop
        req_encoding_crop = req_image_data.encoding_crop
        req_encoding_sqcrop = req_image_data.encoding_squarecrop

        # Start with main RBG color distances to reduce the amount of the rest of the distances to calc
        print('Calculating color distances')
        color_list = []
        for query_result in query_results:
            try:
                image_prod_name = query_result.name
            except:
                image_prod_name = None
            if image_prod_name is not None:
                image_prod_name_arr = image_prod_name.lower().strip('*\'[]\*').split(' ')

                neg_tag_check = False
                for neg_tag in req_tags_negative:
                    neg_tag_check = neg_tag in image_prod_name_arr

                if neg_tag_check is False:
                    req_color_norm_1 = np.array(req_color_1, dtype=int) / np.sum(np.array(req_color_1, dtype=int))
                    req_color_norm_2 = np.array(req_color_2, dtype=int) / np.sum(np.array(req_color_2, dtype=int))
                    query_color_1_norm = np.array(query_result.color_1, dtype=int) / np.sum(
                        np.array(query_result.color_1, dtype=int))
                    query_color_2_norm = np.array(query_result.color_2, dtype=int) / np.sum(
                        np.array(query_result.color_2, dtype=int))
                    query_color_3_norm = np.array(query_result.color_3, dtype=int) / np.sum(
                        np.array(query_result.color_3, dtype=int))

                    # compute the chi-squared distances
                    distance_color_1 = calc_chi_distance(req_color_norm_1, query_color_1_norm)
                    distance_color_2 = calc_chi_distance(req_color_norm_1, query_color_2_norm)
                    distance_color_3 = calc_chi_distance(req_color_norm_1, query_color_3_norm)
                    distance_color_1_2 = calc_chi_distance(req_color_norm_2, query_color_1_norm)
                    distance_color_2_2 = calc_chi_distance(req_color_norm_2, query_color_2_norm)
                    distance_color_3_2 = calc_chi_distance(req_color_norm_2, query_color_3_norm)
                    distance_color = 2 * min([
                        distance_color_1,
                        distance_color_2,
                        distance_color_3
                    ]) + min([
                        distance_color_1_2,
                        distance_color_2_2,
                        distance_color_3_2
                    ])
                    print('Chi distance: ', str(distance_color))

                    distance_color_euc_1 = int(
                        spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                                   np.array(query_result.color_1, dtype=int),
                                                   w=None))
                    distance_color_euc_2 = int(
                        spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                                   np.array(query_result.color_2, dtype=int),
                                                   w=None))
                    distance_color_euc_3 = int(
                        spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                                   np.array(query_result.color_3, dtype=int),
                                                   w=None))

                    distance_color_euc_1_2 = int(
                        spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                                                   np.array(query_result.color_1, dtype=int),
                                                   w=None))
                    distance_color_euc_2_2 = int(
                        spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                                                   np.array(query_result.color_2, dtype=int),
                                                   w=None))
                    distance_color_euc_3_2 = int(
                        spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                                                   np.array(query_result.color_3, dtype=int),
                                                   w=None))

                    distance_color_euc = (1 / 500) * (2 * min([
                        distance_color_euc_1,
                        distance_color_euc_2,
                        distance_color_euc_3
                    ]) + min([
                        distance_color_euc_1_2,
                        distance_color_euc_2_2,
                        distance_color_euc_3_2
                    ]))
                    # distance_color_euc = distance_color_euc_1 + distance_color_euc_2 + distance_color_euc_3
                    print('Euclidean distance: ', str(distance_color_euc))
                    color_query_result = {
                        'query_result': query_result,
                        'img_hash': query_result.img_hash,
                        'color_dist': distance_color_euc + distance_color
                    }
                    color_list.append(color_query_result)

        sorted_color_list = sorted(color_list, key=itemgetter('color_dist'))
        top_color_list = sorted_color_list[0:500]

        # Calculate color_512 vector distances
        print('Calculating color_512 distances')
        color_512_list = []
        for color_result in top_color_list:
            query_result = color_result['query_result']
            color_512_dist = calc_chi_distance(np.array(req_color_512, dtype=float),
                                               np.array(query_result.color_512, dtype=float))

            color_512_result = {
                'query_result': query_result,
                'img_hash': query_result.img_hash,
                'color_dist': color_result['color_dist'],
                'color_512_dist': color_512_dist
            }
            color_512_list.append(color_512_result)

        sorted_color_512_list = sorted(color_512_list, key=itemgetter('color_512_dist'))
        top_color_512_list = sorted_color_512_list[0:400]

        # Calculate encoding vector distances
        print('Calculating no crop encoding distances')
        encoding_list = []
        for color_512_result in top_color_512_list:
            query_result = color_512_result['query_result']
            encoding_nocrop_dist = int(
                spatial.distance.euclidean(np.array(req_encoding_nocrop, dtype=int),
                                           np.array(query_result.encoding_nocrop, dtype=int),
                                           w=None))
            print('encoding_nocrop_dist', str(encoding_nocrop_dist))
            encoding_result = {
                'query_result': query_result,
                'img_hash': query_result.img_hash,
                'color_dist': color_512_result['color_dist'],
                'color_512_dist': color_512_result['color_512_dist'],
                'encoding_nocrop_dist': encoding_nocrop_dist
            }
            encoding_list.append(encoding_result)

        sorted_encoding_list = sorted(encoding_list, key=itemgetter('color_512_dist'))
        top_encoding_list = sorted_encoding_list[0:350]

        # Calculate cropped encoding vector distances
        print('Calculating crop encoding distances')
        encoding_crop_list = []
        for encoding_result in top_encoding_list:
            query_result = encoding_result['query_result']
            encoding_crop_dist = int(
                spatial.distance.euclidean(np.array(req_encoding_crop, dtype=int),
                                           np.array(query_result.encoding_crop, dtype=int),
                                           w=None))
            encoding_result = {
                'query_result': query_result,
                'img_hash': query_result.img_hash,
                'color_dist': encoding_result['color_dist'],
                'color_512_dist': encoding_result['color_512_dist'],
                'encoding_nocrop_dist': encoding_result['encoding_nocrop_dist'],
                'encoding_crop_dist': encoding_crop_dist
            }
            encoding_crop_list.append(encoding_result)

        sorted_encoding_crop_list = sorted(encoding_crop_list, key=itemgetter('encoding_crop_dist'))
        top_encoding_crop_list = sorted_encoding_crop_list[0:300]

        # Calculate square cropped encoding vector distances
        print('Calculating square crop encoding distances')
        encoding_sqcrop_list = []
        for encoding_crop_result in top_encoding_crop_list:
            query_result = encoding_crop_result['query_result']
            encoding_sqcrop_dist = int(
                spatial.distance.euclidean(np.array(req_encoding_sqcrop, dtype=int),
                                           np.array(query_result.encoding_squarecrop, dtype=int),
                                           w=None))
            encoding_result = {
                'query_result': query_result,
                'img_hash': query_result.img_hash,
                'color_dist': encoding_crop_result['color_dist'],
                'color_512_dist': encoding_crop_result['color_512_dist'],
                'encoding_nocrop_dist': encoding_crop_result['encoding_nocrop_dist'],
                'encoding_crop_dist': encoding_crop_result['encoding_crop_dist'],
                'encoding_sqcrop_dist': encoding_sqcrop_dist
            }
            encoding_sqcrop_list.append(encoding_result)

        # Make sure we return the original request image back on top
        if not any(d['img_hash'] == req_img_hash for d in encoding_sqcrop_list):
            print('Product not in list, need to add')
            encoding_sqcrop_list.insert(0, {
                'img_hash': req_img_hash,
                'query_result': req_image_data,
                'encoding_sqcrop_dist': -1000,
                'color_dist': -1000
            })
        else:
            print('Product already in list, need to make sure its on top')
            request_prod = next(item for item in encoding_sqcrop_list if item['img_hash'] == req_img_hash)
            request_prod['color_dist'] = -1000
            request_prod['encoding_sqcrop_dist'] = -1000

        sorted_encoding_sqcrop_list = sorted(encoding_sqcrop_list, key=itemgetter('encoding_sqcrop_dist'))
        top_encoding_sqcrop_list = sorted_encoding_sqcrop_list[0:100]

        top_encoding_sqcrop_list = sorted(top_encoding_sqcrop_list, key=itemgetter('color_dist'))
        top_encoding_sqcrop_list = top_encoding_sqcrop_list[0:30]

        # Serialize the results and return as array
        result_list = []
        prod_check = set()
        for obj in top_encoding_sqcrop_list:
            result_img_hash = obj['img_hash']
            prod_search = db.session.query(Products).filter(Products.img_hashes.any(result_img_hash)).first()
            prod_hash = prod_search.prod_hash
            if prod_hash not in prod_check:
                prod_serial = ProductsSchema().dump(prod_search)
                prod_check.add(prod_hash)
                img_serial = ImageSchema().dump(obj['query_result'])
                result_dict = {
                    'prod_serial': prod_serial,
                    'image_data': img_serial
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


def search_from_upload_v2(request, db, ImagesV2, ProductsV2):
    data = request.get_json(force=True)
    data = json.loads(data)
    print('Request received')
    req_tags = data['tags']
    req_sex = data['sex']
    req_shop_excl = data['no_shop']
    req_color_1 = data['color_1']
    req_color_2 = data['color_2']
    req_encoding = data['encoding_rcnn']

    conditions = []
    req_color_arr_1 = np.asarray(req_color_1)
    req_color_arr_2 = np.asarray(req_color_2)
    req_encoding_arr = np.asarray(req_encoding)
    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    all_cats = tag_list.all_cats
    kind_search_cats = [req_tag for req_tag in req_tags if req_tag in kind_cats]
    all_cat_search_arr = np.zeros(len(all_cats))
    for req_tag in req_tags:
        if req_tag in all_cats:
            all_cat_search_arr[all_cats.index(req_tag)] = 1

    for kind_search_cat in kind_search_cats:
        conditions.append(
            func.lower(ImagesV2.name).ilike('%{}%'.format(kind_search_cat)) | ImagesV2.kind_cats.any(kind_search_cat)
        )
    conditions.append(
        (ImagesV2.sex == req_sex)
    )
    if len(req_shop_excl) > 0:
        conditions.append(
            (ImagesV2.shop != any_(req_shop_excl))
        )

    print('Querying database...')
    query = db.session.query(
        ImagesV2.name,
        ImagesV2.img_hash,
        ImagesV2.color_1,
        ImagesV2.color_1_hex,
        ImagesV2.color_2,
        ImagesV2.color_2_hex,
        ImagesV2.color_3,
        ImagesV2.color_3_hex,
        ImagesV2.encoding_crop,
        ImagesV2.all_arr
    ).filter(
        and_(*conditions)
    )

    query_results = query.order_by(func.random()).limit(2000).all()
    if len(query_results) == 0:
        return 'no results'
    else:
        print('Query results obtained')

        # img_hashes = []
        all_cat_arrays = []
        for query_result in query_results:
            # img_hashes.append(query_result.img_hash)
            # print(query_result.all_arr)
            all_cat_arrays.append(query_result.all_arr)
            # print(len(query_result.all_arr))
        all_cat_matrix = np.asarray(all_cat_arrays)
        print(f'all_cat_matrix.shape : {all_cat_matrix.shape}')
        print(f'all_cat_search_arr.shape : {all_cat_search_arr.shape}')
        similarity_matrix = np.sum(all_cat_matrix * all_cat_search_arr, axis=1)
        closest_n_indices = similarity_matrix.argsort()[-500:][::-1]
        closest_n_results = [query_results[x] for x in closest_n_indices]
        print('Closest all cats calculated')
        color_1_arrays = []
        color_2_arrays = []
        color_3_arrays = []
        for closest_n_result in closest_n_results:
            color_1_arrays.append(closest_n_result.color_1)
            color_2_arrays.append(closest_n_result.color_2)
            color_3_arrays.append(closest_n_result.color_3)
        color_1_matrix = np.asarray(color_1_arrays)
        color_2_matrix = np.asarray(color_2_arrays)
        color_3_matrix = np.asarray(color_3_arrays)

        dist_color_1_1_arr = np.linalg.norm(color_1_matrix - req_color_arr_1, axis=1)
        dist_color_1_2_arr = np.linalg.norm(color_1_matrix - req_color_arr_2, axis=1)
        dist_color_2_1_arr = np.linalg.norm(color_2_matrix - req_color_arr_1, axis=1)
        dist_color_2_2_arr = np.linalg.norm(color_2_matrix - req_color_arr_2, axis=1)
        dist_color_3_1_arr = np.linalg.norm(color_3_matrix - req_color_arr_1, axis=1)
        dist_color_3_2_arr = np.linalg.norm(color_3_matrix - req_color_arr_2, axis=1)

        combined_color_dist_arr = dist_color_1_1_arr + 0.5 * dist_color_1_2_arr + 0.5 * dist_color_2_1_arr + \
                                  0.4 * dist_color_2_2_arr + 0.3 * dist_color_3_1_arr + 0.2 * dist_color_3_2_arr

        closest_n_color_ind = combined_color_dist_arr.argsort()[:150]
        closest_n_color_results = [closest_n_results[x] for x in closest_n_color_ind]
        print('Closest colors calculated')
        encoding_arrays = []
        for closest_n_color_result in closest_n_color_results:
            encoding_arrays.append(closest_n_color_result.encoding_crop)
        encoding_matrix = np.asarray(encoding_arrays)

        dist_encoding_arr = np.linalg.norm(encoding_matrix - req_encoding_arr, axis=1)
        closest_n_enc_ind = dist_encoding_arr.argsort()[:30]
        closest_n_enc_results = [closest_n_color_results[x] for x in closest_n_enc_ind]
        print('Closest encodings calculated')
        result_list = []
        prod_check = set()

        for closest_n_enc_result in closest_n_enc_results:
            result_img_hash = closest_n_enc_result[1]

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
                    'prod_serial': prod_serial,
                    'image_data': img_serial
                }
                result_list.append(result_dict)
        print('Results obtained from DB')

        return result_list


# POST request handling function to search similar images from an image uploaded by user
def search_from_upload(request, db, Images, Products):
    data = request.get_json(force=True)
    data = json.loads(data)

    req_tags = data['tags']
    req_sex = data['sex']
    req_shop_excl = data['no_shop']
    req_color_1 = data['color_1']
    req_color_2 = data['color_2']
    # req_color_512 = request.args.get('color_512').strip('\'[]').split(',')
    req_encoding = data['encoding_nocrop']
    # req_encoding_crop = request.args.get('encoding_crop').strip('\'[]').split(',')
    # req_encoding_sqcrop = req_data['encoding_squarecrop']

    print('Assembling db query conditions')
    # Assemble DB query conditions in array from tags
    conditions = []
    for tag in req_tags:
        conditions.append(
            func.lower(Images.name).ilike('%{}%'.format(tag)) | Images.img_cats_ai_txt.any(
                tag) | Images.img_cats_sc_txt.any(tag)
        )
    conditions.append(
        (Images.sex == req_sex)
    )
    if len(req_shop_excl) > 0:
        conditions.append(
            (Images.shop != any_(req_shop_excl))
        )
    print('Query db')
    # Use those conditions as argument for a filter function
    query = db.session.query(
        Images.name,
        Images.img_hash,
        Images.color_1,
        Images.color_1_hex,
        Images.color_2,
        Images.color_2_hex,
        Images.color_3,
        Images.color_3_hex,
        Images.encoding_nocrop
    ).filter(
        and_(*conditions)
    )
    query_results = query.order_by(func.random()).limit(2000).all()

    if len(query_results) == 0:
        return 'no results'
    else:
        print('Calculating color distances')
        # Start with main RBG color distances to reduce the amount of the rest of the distances to calc
        color_list = []
        for query_result in query_results:
            try:
                image_prod_name = query_result.name
            except:
                image_prod_name = None
            if image_prod_name is not None:
                req_color_norm_1 = np.array(req_color_1, dtype=int) / np.sum(np.array(req_color_1, dtype=int))
                req_color_norm_2 = np.array(req_color_2, dtype=int) / np.sum(np.array(req_color_2, dtype=int))
                query_color_1_norm = np.array(query_result.color_1, dtype=int) / np.sum(
                    np.array(query_result.color_1, dtype=int))
                query_color_2_norm = np.array(query_result.color_2, dtype=int) / np.sum(
                    np.array(query_result.color_2, dtype=int))
                query_color_3_norm = np.array(query_result.color_3, dtype=int) / np.sum(
                    np.array(query_result.color_3, dtype=int))

                # compute the chi-squared distances
                distance_color_1 = calc_chi_distance(req_color_norm_1, query_color_1_norm)
                distance_color_2 = calc_chi_distance(req_color_norm_1, query_color_2_norm)
                distance_color_3 = calc_chi_distance(req_color_norm_1, query_color_3_norm)
                distance_color_1_2 = calc_chi_distance(req_color_norm_2, query_color_1_norm)
                distance_color_2_2 = calc_chi_distance(req_color_norm_2, query_color_2_norm)
                distance_color_3_2 = calc_chi_distance(req_color_norm_2, query_color_3_norm)
                distance_color = 2 * min([
                    distance_color_1,
                    distance_color_2,
                    distance_color_3
                ]) + min([
                    distance_color_1_2,
                    distance_color_2_2,
                    distance_color_3_2
                ])
                print('Chi distance: ', str(distance_color))

                distance_color_euc_1 = int(
                    spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                               np.array(query_result.color_1, dtype=int),
                                               w=None))
                distance_color_euc_2 = int(
                    spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                               np.array(query_result.color_2, dtype=int),
                                               w=None))
                distance_color_euc_3 = int(
                    spatial.distance.euclidean(np.array(req_color_1, dtype=int),
                                               np.array(query_result.color_3, dtype=int),
                                               w=None))

                distance_color_euc_1_2 = int(
                    spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                                               np.array(query_result.color_1, dtype=int),
                                               w=None))
                distance_color_euc_2_2 = int(
                    spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                                               np.array(query_result.color_2, dtype=int),
                                               w=None))
                distance_color_euc_3_2 = int(
                    spatial.distance.euclidean(np.array(req_color_2, dtype=int),
                                               np.array(query_result.color_3, dtype=int),
                                               w=None))

                distance_color_euc = (1 / 500) * (2 * min([
                    distance_color_euc_1,
                    distance_color_euc_2,
                    distance_color_euc_3
                ]) + min([
                    distance_color_euc_1_2,
                    distance_color_euc_2_2,
                    distance_color_euc_3_2
                ]))
                print('Euclidean distance: ', str(distance_color_euc))
                color_query_result = {
                    'query_result': query_result,
                    'img_hash': query_result.img_hash,
                    'color_dist': distance_color_euc + distance_color
                }
                color_list.append(color_query_result)

        sorted_color_list = sorted(color_list, key=itemgetter('color_dist'))
        top_color_list = sorted_color_list[0:300]

        # # Calculate color_512 vector distances
        # color_512_list = []
        # for color_result in top_color_list:
        #     query_result = color_result['query_result']
        #     color_512_dist = calc_distance(np.array(req_color_512, dtype=float), np.array(query_result.color_512, dtype=float))
        #     print('Color 512 distance:', str(color_512_dist))
        #     color_512_result = {
        #         'query_result': query_result,
        #         'color_dist': color_result['color_dist'],
        #         'color_512_dist': color_512_dist,
        #         'img_hash': query_result.img_hash
        #     }
        #     color_512_list.append(color_512_result)
        #
        # sorted_color_512_list = sorted(color_512_list, key=itemgetter('color_512_dist'))
        # top_color_512_list = sorted_color_512_list[0:100]

        # Calculate no crop encoding vector distances
        nocropenc_list = []
        for color_512_result in top_color_list:
            query_result = color_512_result['query_result']
            encoding_dist = int(
                spatial.distance.euclidean(np.array(req_encoding, dtype=int),
                                           np.array(query_result.encoding_nocrop, dtype=int),
                                           w=None))
            encoding_result = {
                'query_result': query_result,
                'color_dist': color_512_result['color_dist'],
                'img_hash': query_result.img_hash,
                'encoding_dist': encoding_dist
            }
            nocropenc_list.append(encoding_result)

        sorted_nocropenc_list = sorted(nocropenc_list, key=itemgetter('encoding_dist'))
        top_nocropenc_list = sorted_nocropenc_list[0:150]

        # print('Calculating encoding distances')
        # # Calculate crop encoding vector distances
        # encoding_list = []
        # for color_512_result in top_color_512_list:
        #     query_result = color_512_result['query_result']
        #     encoding_dist = int(
        #         spatial.distance.euclidean(np.array(req_encoding_crop, dtype=int),
        #                                    np.array(query_result.encoding_crop, dtype=int),
        #                                    w=None))
        #     print('Encoding distance', str(encoding_dist))
        #     encoding_result = {
        #         'query_result': query_result,
        #         'img_hash': query_result.img_hash,
        #         'color_dist': color_512_result['color_dist'],
        #         'encoding_dist': encoding_dist
        #     }
        #     encoding_list.append(encoding_result)

        # sorted_encoding_list = sorted(encoding_list, key=itemgetter('encoding_dist'))
        # top_encoding_list = sorted_encoding_list[0:80]

        sorted_topcolor_list = sorted(top_nocropenc_list, key=itemgetter('color_dist'))
        top_topcolor_list = sorted_topcolor_list[0:30]

        # # Calculate cropped encoding vector distances
        # encoding_crop_list = []
        # for encoding_result in top_encoding_list:
        #     query_result = encoding_result['query_result']
        #     encoding_crop_dist = int(
        #         spatial.distance.euclidean(np.array(req_encoding_crop, dtype=int),
        #                                    np.array(query_result.encoding_crop, dtype=int),
        #                                    w=None))
        #     encoding_result = {
        #         'query_result': query_result,
        #         'color_dist': encoding_result['query_result'],
        #         'color_512_dist': encoding_result['color_512_dist'],
        #         'encoding_dist': encoding_result['encoding_dist'],
        #         'encoding_crop_dist': encoding_crop_dist
        #     }
        #     encoding_crop_list.append(encoding_result)
        #
        # sorted_encoding_crop_list = sorted(encoding_crop_list, key=itemgetter('encoding_crop_dist'))
        # top_encoding_crop_list = sorted_encoding_crop_list[0:100]
        #
        # # Calculate square cropped encoding vector distances
        # encoding_sqcrop_list = []
        # for encoding_crop_result in top_encoding_crop_list:
        #     query_result = encoding_crop_result['query_result']
        #     encoding_sqcrop_dist = int(
        #         spatial.distance.euclidean(np.array(req_encoding_sqcrop, dtype=int),
        #                                    np.array(query_result.encoding_squarecrop, dtype=int),
        #                                    w=None))
        #     encoding_result = {
        #         'query_result': query_result,
        #         'color_dist': encoding_crop_result['query_result'],
        #         'color_512_dist': encoding_crop_result['color_512_dist'],
        #         'encoding_dist': encoding_crop_result['encoding_dist'],
        #         'encoding_crop_dist': encoding_crop_result['encoding_crop_dist'],
        #         'encoding_sqcrop_dist': encoding_sqcrop_dist
        #     }
        #     encoding_sqcrop_list.append(encoding_result)
        #
        # sorted_encoding_sqcrop_list = sorted(encoding_sqcrop_list, key=itemgetter('encoding_sqcrop_dist'))
        # top_encoding_sqcrop_list = sorted_encoding_sqcrop_list[0:50]

        # Serialize the results and return as array
        result_list = []
        prod_check = set()
        for obj in top_topcolor_list:
            result_img_hash = obj['img_hash']
            prod_search = db.session.query(Products).filter(Products.img_hashes.any(result_img_hash)).first()
            prod_hash = prod_search.prod_hash
            if prod_hash not in prod_check:
                prod_serial = ProductsSchema().dump(prod_search)
                prod_check.add(prod_hash)
                img_serial = ImageSchema().dump(obj['query_result'])
                result_dict = {
                    'prod_serial': prod_serial,
                    'image_data': img_serial
                }
                result_list.append(result_dict)

        return result_list


def db_text_search(request, db, Products, Images):
    search_string = request.args.get('search_string')
    print('search string: ' + search_string)
    search_string.replace('+', ' ')
    sex = request.args.get('sex')

    string_list = search_string.strip().lower().split()
    linking_words = ['with', 'on', 'under', 'over', 'at', 'like', 'in', 'for', 'as', 'after', 'by', 'and']
    string_list_clean = [e for e in string_list if e not in linking_words]
    print('Cleaned string list', str(string_list_clean))
    color_word_dict = color_check(string_list_clean)
    color_list = color_word_dict['colors']
    word_list = color_word_dict['words']
    search_string_clean = ' '.join(word_list)

    query_results = []
    if len(color_list) > 0 and len(word_list) > 0:
        query_results += db.session.query(Images).filter(func.lower(Images.name).op('%%')(search_string_clean)
                                                         & func.lower(Images.color_name).op('%%')(color_list[0])) \
            .filter(Images.sex == sex).limit(30).all()
    else:
        query_results += db.session.query(Images).filter(func.lower(Images.name).op('%%')(search_string_clean)) \
            .filter(Images.sex == sex).limit(30).all()

    if len(query_results) < 5:
        query_results += db.session.query(Images).filter(
            func.lower(Images.name).op('%%')(' '.join(string_list_clean))) \
            .filter(Images.sex == sex).limit(30).all()
    if len(query_results) < 5:
        query_results += db.session.query(Images).filter(
            func.lower(Images.name).op('%%')(search_string_clean)) \
            .filter(Images.sex == sex).limit(30).all()

    img_list = []
    for query_result in query_results:
        img_query_result = {
            'query_result': query_result,
            'img_hash': query_result.img_hash
        }
        img_list.append(img_query_result)

    result_list = []
    prod_check = set()
    for obj in img_list:
        result_img_hash = obj['img_hash']
        prod_search = db.session.query(Products).filter(Products.img_hashes.any(result_img_hash)).first()
        prod_hash = prod_search.prod_hash
        if prod_hash not in prod_check:
            prod_serial = ProductsSchema().dump(prod_search)
            prod_check.add(prod_hash)
            img_serial = ImageSchema().dump(obj['query_result'])
            result_dict = {
                'prod_serial': prod_serial,
                'image_data': img_serial
            }
            result_list.append(result_dict)

    # Make it HTTP friendly
    res = jsonify(res=result_list, tags=word_list)
    return res

# def db_explorer_search(data, db, Images, Products):
#     main_cat_top = data['main_cat_top']
#     main_cat_sub = data['main_cat_sub']
#     sex = data['sex']
#     color_selected = data['color_selected']
#     req_color = []
#     if color_selected:
#         color_dict = data['color']
#         req_color.append(color_dict['r'])
#         req_color.append(color_dict['g'])
#         req_color.append(color_dict['b'])
#
#     shops = data['shops']
#     brands = data['brands']
#     max_price = float(data['max_price'])
#
#     if brands[0] == 'All':
#         id_list = db.session.query(Product).filter(
#             ((Product.img_cats_ai_txt.any(main_cat_sub))
#              | (Product.spider_cat == main_cat_sub)
#              | (Product.img_cats_sc_txt.any(main_cat_sub)))
#             & ((Product.img_cats_ai_txt.any(main_cat_top))
#                | (Product.spider_cat == main_cat_top)
#                | (Product.img_cats_sc_txt.any(main_cat_top)))
#             & (Product.sex == sex)
#             & (or_(*[Product.shop.ilike(shop) for shop in shops]))
#             & (Product.price <= max_price)
#         ).order_by(
#             func.random()).limit(5000).all()
#
#         if len(id_list) < 100:
#             id_list = db.session.query(Product).filter(
#                 ((Product.img_cats_ai_txt.any(main_cat_sub))
#                  | (Product.spider_cat == main_cat_sub)
#                  | (Product.img_cats_sc_txt.any(main_cat_sub)))
#                 & (Product.sex == sex)
#                 & (or_(*[Product.shop.ilike(shop) for shop in shops]))
#                 & (Product.price <= max_price)
#             ).order_by(
#                 func.random()).limit(5000).all()
#
#     else:
#         id_list = db.session.query(Product).filter(
#             ((Product.img_cats_ai_txt.any(main_cat_sub))
#              | (Product.spider_cat == main_cat_sub)
#              | (Product.img_cats_sc_txt.any(main_cat_sub)))
#             & ((Product.img_cats_ai_txt.any(main_cat_top))
#                | (Product.spider_cat == main_cat_top)
#                | (Product.img_cats_sc_txt.any(main_cat_top)))
#             & (Product.sex == sex)
#             & (or_(*[Product.shop.ilike(shop) for shop in shops]))
#             & (Product.price <= max_price)
#             & (or_(*[Product.brand.ilike(brand) for brand in brands]))
#         ).order_by(
#             func.random()).limit(5000).all()
#
#         if len(id_list) < 100:
#             id_list = db.session.query(Product).filter(
#                 ((Product.img_cats_ai_txt.any(main_cat_sub))
#                  | (Product.spider_cat == main_cat_sub)
#                  | (Product.img_cats_sc_txt.any(main_cat_sub)))
#                 & (Product.sex == sex)
#                 & (or_(*[Product.shop.ilike(shop) for shop in shops]))
#                 & (Product.price <= max_price)
#                 & (or_(*[Product.brand.ilike(brand) for brand in brands]))
#             ).order_by(
#                 func.random()).limit(5000).all()
#
#     if color_selected:
#         color_dist_list = []
#         for prod_obj in id_list:
#             color_prod_id = prod_obj.id
#             color1_rgb = prod_obj.color_1
#             color2_rgb = prod_obj.color_2
#             color3_rgb = prod_obj.color_3
#
#             distance_color_1 = int(
#                 spatial.distance.euclidean(np.array(req_color, dtype=int), np.array(color1_rgb, dtype=int),
#                                            w=None))
#             distance_color_2 = int(
#                 spatial.distance.euclidean(np.array(req_color, dtype=int), np.array(color2_rgb, dtype=int),
#                                            w=None))
#             distance_color_3 = int(
#                 spatial.distance.euclidean(np.array(req_color, dtype=int), np.array(color3_rgb, dtype=int),
#                                            w=None))
#
#             color_dist = int((distance_color_1 + distance_color_2 + distance_color_3) / 3)
#
#             item_obj = {
#                 'id': color_prod_id,
#                 'color_distance': color_dist
#             }
#
#             color_dist_list.append(item_obj)
#
#         # Closest colors at top
#         sorted_color_list = sorted(color_dist_list, key=itemgetter('color_distance'))
#         top_color_list = sorted_color_list[0:100]
#
#     else:
#         shuffle(id_list)
#
#         random_list = []
#         counter = 0
#         for prod_obj in id_list:
#             counter += 1
#
#             if counter < 100:
#                 prod_id = prod_obj.id
#                 item_obj = {
#                     'id': prod_id
#                 }
#
#                 random_list.append(item_obj)
#
#         top_color_list = random_list
#
#     # Declare Marshmallow schema so that SqlAlchemy object can be serialized
#     product_schema = ProductSchema()
#
#     result_list = []
#     for obj in top_color_list:
#         result_obj_id = obj['id']
#         prod_search = db.session.query(Product).filter((Product.id == result_obj_id)).first()
#         prod_serial = product_schema.dump(prod_search)
#         result_list.append(prod_serial)

#
# def db_text_search(request, XXXX, XXXX):
#     search_string = request.args.get('string')
#     sex = request.args.get('sex')
#
#     print('Text search with string: ', str(search_string))
#     # cleaned_string = search_string.translate(' ', "!@£$%^&*()<>?/|~`.,:;#+=_")
#
#     string_list = search_string.strip().lower().split()
#     print('string list', str(string_list))
#     linking_words = ['with', 'on', 'under', 'over', 'at', 'like', 'in', 'for', 'as', 'after']
#
#     string_list_clean = [e for e in string_list if e not in linking_words]
#
#     color_word_dict = color_check(string_list_clean)
#
#     print(color_word_dict)
#     word_list = color_word_dict['words']
#     color_list = color_word_dict['colors']
#
#     id_list = []
#     if 2 > len(word_list) > 0 and len(color_list) > 0:
#         print('1 word and is color')
#         id_list += db.session.query(Product).filter(
#             (Product.sex == sex) & (func.lower(Product.name).contains(word_list[-1])) & (
#                 func.lower(Product.color_name).contains(color_list[0]))).order_by(func.random()).limit(60).all()
#
#     elif 3 > len(word_list) > 1 and len(color_list) > 0:
#         print('2 words and is color')
#         id_list += db.session.query(Product).filter(
#             (Product.sex == sex) & (func.lower(Product.name).contains(word_list[-1])) & (
#                 func.lower(Product.name).contains(word_list[1])) & (
#                 func.lower(Product.color_name).contains(
#                     color_list[0]))).order_by(func.random()).limit(60).all()
#
#     elif 3 > len(word_list) > 1:
#         print('2 words, no color')
#         id_list += db.session.query(Product).filter(
#             (Product.sex == sex) & (func.lower(Product.name).contains(word_list[0])) & (
#                 func.lower(Product.name).contains(word_list[1]))).order_by(func.random()).limit(60).all()
#
#     elif 4 > len(word_list) > 2:
#         print('3 words, no color')
#         id_list += db.session.query(Product).filter(
#             (Product.sex == sex) & (func.lower(Product.name).contains(word_list[0])) & (
#                 func.lower(Product.name).contains(word_list[1])) & (
#                 func.lower(Product.name).contains(word_list[2]))).order_by(
#             func.random()).limit(60).all()
#         # word_len = len(word_list)
#         # for i in range(0, word_len):
#         #     id_list += db.session.query(Product).filter(
#         #         (func.lower(Product.name).contains(word_list[i]))).order_by(
#         #         func.random()).limit(30).all()
#     elif 2 > len(word_list) > 0:
#         print('1 word, no color')
#         id_list += db.session.query(Product).filter(
#             (Product.sex == sex) & (func.lower(Product.name).contains(word_list[-1]))).order_by(
#             func.random()).limit(60).all()
#
#     elif len(color_list) > 0:
#         print('only color')
#         color_len = len(color_list)
#         for k in range(0, color_len):
#             id_list += db.session.query(Product).filter(
#                 (Product.sex == sex) & (func.lower(Product.color_name).contains(color_list[k]))).order_by(
#                 func.random()).limit(60).all()
#
#     else:
#         return json.dumps('BAD REQUEST')
#
#     # Declare Marshmallow schema so that SqlAlchemy object can be serialized
#     product_schema = ProductSchema()
#
#     result_list = []
#     for prod_id in id_list:
#         # prod_id_str = str(prod_id)
#         # text_prod_id = re.search('(?<=id=\[).{0,8}(?=\])', prod_id_str)[0]
#         text_prod_id = prod_id.id
#         prod_search = db.session.query(Product).filter((Product.id == text_prod_id)).first()
#         prod_serial = product_schema.dump(prod_search)
#         result_list.append(prod_serial)
#
#     main_cat = ''
#     if len(word_list) > 0:
#         main_cat = word_list[-1]
#
#     # Make it HTTP friendly
#     res = jsonify(res=result_list, mainCat=main_cat)
