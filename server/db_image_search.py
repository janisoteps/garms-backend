# from sqlalchemy import func, any_, and_, or_
# from marshmallow_schema import ImagesFullWomenASchema, ImagesFullMenASchema, ProductsWomenASchema, ProductsMenASchema
# import scipy.spatial as spatial
# import numpy as np
# from numpy.linalg import norm
# from operator import itemgetter
# import json
# from flask import jsonify
# import data.cats as cats
# import data.colors as colors
#
#
# def calc_chi_distance(hist_1, hist_2, eps=1e-10):
#     # compute the chi-squared distance
#     distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_1, hist_2)])
#
#     return distance
#
#
# def calc_cross_entropy(vector_1, vector_2):
#     dist = np.sum(vector_1 * np.log(vector_2) + (1 - vector_1) * np.log(1 - vector_2))
#
#     return dist
#
#
# def search_from_upload(request, db, Images, ImagesSkinny, Products):
#     data = request.get_json(force=True)
#     data = json.loads(data)
#     print('Request received')
#     req_tags = data['tags']
#     req_sex = data['sex']
#     # req_shop_excl = data['no_shop']
#     req_color_1 = data['color_1']
#     # req_color_2 = data['color_2']
#     # req_encoding = data['encoding_rcnn']
#     req_vgg16_encoding = data['vgg16_encoding']
#
#     result_limit = 2000
#
#     req_vgg16_encoding_arr = np.asarray(req_vgg16_encoding)
#
#     base_conditions = []
#     cat_conditions = []
#
#     for req_tag in req_tags:
#         cat_conditions.append(
#             ImagesSkinny.name.ilike('%{}%'.format(req_tag))
#         )
#     base_conditions.append(
#         ImagesSkinny.is_deleted.isnot(True)
#     )