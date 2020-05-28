from sqlalchemy import func, any_, and_, or_
from marshmallow_schema import ImagesFullSchema, ProductsSchema
import numpy as np
from numpy.linalg import norm
from operator import itemgetter
import data.cats as cats


def calc_chi_distance(hist_1, hist_2, eps=1e-10):
    # compute the chi-squared distance
    distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_1, hist_2)])

    return distance


def calc_cross_entropy(vector_1, vector_2):
    dist = np.sum(vector_1 * np.log(vector_2) + (1 - vector_1) * np.log(1 - vector_2))

    return dist


def db_search_from_image(request, db, ImagesFull, ImagesSkinny, Products):
    data = request.get_json(force=True)
    print('Request received')
    req_pos_tags = data['pos_tags']
    req_neg_tags = data['neg_tags']
    req_sex = data['sex']
    req_color_1 = data['color_1']
    req_vgg16_encoding = data['vgg16_encoding']
    prev_prod_ids = data['prev_prod_ids']
    max_price = int(data['max_price'])
    req_brands = data['brands']
    result_limit = 2000

    tag_list = cats.Cats()
    kind_cats = tag_list.kind_cats
    kind_cats_search = []
    for word in req_pos_tags:
        for cat in kind_cats:
            if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                kind_cats_search.append(cat)
    print('all cats')
    print(req_pos_tags)
    print('kind_cats_search')
    print(kind_cats_search)
    print('max price')
    print(max_price)
    print('color')
    print(req_color_1)

    base_conditions = []
    kind_cat_conditions = []
    cat_conditions = []

    maternity_tags = ['mom', 'mum', 'mamalicious', 'maternity']
    is_maternity = False
    for req_tag in req_pos_tags:
        if req_tag in kind_cats_search:
            kind_cat_conditions.append(
                (ImagesSkinny.kind_cats.any(req_tag))
            )
        else:
            cat_conditions.append(
                ImagesSkinny.name.ilike('%{}%'.format(req_tag))
            )
        if req_tag in maternity_tags:
            is_maternity = True

    for req_neg_tag in req_neg_tags:
        cat_conditions.append(
            (~ImagesSkinny.name.ilike('%{}%'.format(req_neg_tag)))
        )
    if is_maternity is False:
        for maternity_tag in maternity_tags:
            cat_conditions.append(
                (~ImagesSkinny.name.ilike('%{}%'.format(maternity_tag)))
            )
    base_conditions.append(
        ImagesSkinny.is_deleted.isnot(True)
    )
    if prev_prod_ids is not None:
        for prev_prod_id in prev_prod_ids:
            base_conditions.append(
                ImagesSkinny.prod_id != prev_prod_id
            )
    if len(req_brands) > 0:
        for req_brand in req_brands:
            req_brand_lower = req_brand.lower()
            base_conditions.append(
                (func.lower(ImagesSkinny.brand).ilike('%{0}%'.format(req_brand_lower)))
            )
    if max_price < 1000000:
        base_conditions.append(
            or_(
                (ImagesSkinny.price < max_price),
                and_(
                    (ImagesSkinny.sale == True), (ImagesSkinny.saleprice < max_price)
                )
            )
        )

    query_results = db.session.query(ImagesSkinny, ImagesFull).filter(
        ImagesSkinny.img_hash == ImagesFull.img_hash
    ).filter(
        and_(
            and_(*base_conditions),
            and_(*kind_cat_conditions),
            and_(*cat_conditions)
        )
    ).limit(result_limit).all()

    print(f'RESULT LENGTH: {len(query_results)}')
    if len(query_results) == 0:
        return []
    else:
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

        target_color_matrix = np.broadcast_to(np.array(req_color_1), color_1_matrix.shape)
        target_color_arr = np.asarray(req_color_1)
        target_encoding_arr = np.asarray(req_vgg16_encoding)
        euclidean_factor = 5000 if np.sum(target_color_arr) > 250 else 800
        print(f'euclidean_factor: {euclidean_factor}')

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
        closest_color_idx = color_dist_total.argsort()[0:int(len(query_results) / 2)]
        closest_n_results_color = [{
            'query_result': query_results[idx][1],
            'color_dist': color_dist_total[idx]
        } for idx in closest_color_idx]
        print(f'Closest colors calculated, length: {len(closest_n_results_color)}')

        for query_result_dict in closest_n_results_color:
            vgg16_enc_list.append(query_result_dict['query_result'].encoding_vgg16)
        vgg16_enc_matrix = np.array(vgg16_enc_list)

        dist_encoding_arr = np.linalg.norm(vgg16_enc_matrix - target_encoding_arr, axis=1)
        closest_n_enc_ind = dist_encoding_arr.argsort()[0:int(len(query_results) / 4)]
        closest_n_results_enc = [closest_n_results_color[x] for x in closest_n_enc_ind]
        print(f'Closest encodings calculated, length: {len(closest_n_results_enc)}')

        top_encoding_list = sorted(closest_n_results_enc, key=itemgetter('color_dist'))
        top_encoding_list = top_encoding_list[0:80]

        # Serialize the results and return as array
        result_list = []
        prod_check = set()
        print('Obtaining result data')
        for result_dict in top_encoding_list:
            img_query_result = result_dict['query_result']
            result_prod_id = img_query_result.prod_id
            # prod_search = db.session.query(Products).filter(Products.prod_id == result_prod_id).first()
            # if prod_search is not None:
            prod_hash = img_query_result.prod_id
            if prod_hash not in prod_check:
                # prod_serial = ProductsSchema().dump(prod_search)
                prod_check.add(prod_hash)
                img_serial = ImagesFullSchema().dump(img_query_result)
                result_dict = {
                    'prod_serial': [],
                    'image_data': img_serial[0]
                }
                result_list.append(result_dict)

        return result_list
