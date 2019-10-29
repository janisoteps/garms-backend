import os
from sqlalchemy import func


# Iterate through all rows in Image db and recalculate kind, filter and all_cats columns
class CatTransform:
    def cat_transform(self, cats, db, ImagesV2, data):
        key_string = os.environ['TRANSFORM_KEY']
        shop = data['shop']
        if data['transform_key'] == key_string:

            cat_list = cats.Cats()
            all_cats = cat_list.all_cats
            kind_cats = cat_list.kind_cats
            filter_cats = cat_list.filter_cats

            img_hashes = db.session.query(
                ImagesV2.img_hash
            ).filter(
                ImagesV2.shop == shop
            ).order_by(func.random()).all()

            counter = 0
            for img_hash in img_hashes:
                counter += 1
                print(f'count : {counter}')
                query_result = ImagesV2.query.filter_by(img_hash=img_hash).first()

                if len(query_result.all_arr) != len(all_cats):
                    kind_arr = [0] * len(kind_cats)
                    filter_arr = [0] * len(filter_cats)
                    all_arr = [0] * len(all_cats)
                    filter_list = []

                    for kind_cat in query_result.kind_cats:
                        if kind_cat in kind_cats:
                            kind_arr[kind_cats.index(kind_cat)] = 1
                    # print('query_result.kind_arr')
                    # print(query_result.kind_arr)
                    # print('kind_arr')
                    # print(kind_arr)
                    query_result.kind_arr = kind_arr

                    name_list = query_result.name.lower().split(' ')
                    for word in name_list:
                        if word in filter_cats:
                            filter_arr[filter_cats.index(word)] = 1
                            filter_list.append(word)
                    query_result.filter_cats = filter_list
                    query_result.filter_arr = filter_arr

                    all_result_cats = filter_list + query_result.kind_cats + query_result.color_pattern_cats \
                                      + query_result.style_cats + query_result.material_cats + query_result.attribute_cats
                    query_result.all_cats = all_result_cats
                    for all_result_cat in all_result_cats:
                        if all_result_cat in all_cats:
                            all_arr[all_cats.index(all_result_cat)] = 1
                    query_result.all_arr = all_arr

                    print(f'name : {query_result.name}')

                    db.session.commit()

        return True
