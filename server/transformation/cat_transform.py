import os
from sqlalchemy import func


def cat_clean_transform(cats, db, ImagesSkinny, data):
    exceptions = [
        'maternity',
        'tall',
        'curve',
        'plus',
        'petite',
        'mamalicious'
    ]
    transform_key = os.environ['TRANSFORM_KEY']
    if data['transform_key'] == transform_key:

        cat_class = cats.Cats()

        img_hashes = db.session.query(
            ImagesSkinny.img_hash
        ).order_by(func.random()).all()

        total_count = len(img_hashes)
        counter = 0
        for img_hash in img_hashes:
            counter += 1
            print(f'row : {counter}')
            print(f'from : {total_count}')
            query_result = ImagesSkinny.query.filter_by(img_hash=img_hash).first()

            brand = query_result.brand
            print(f'BRAND: {brand}')
            brand_word_list = brand.lower().split(' ')
            brand_word_list = [word.replace('*', '') for word in brand_word_list]

            name = query_result.name
            print(f'NAME: {name}')
            name_word_list = name.lower().split(' ')
            name_word_list = [word.replace('*', '') for word in name_word_list]

            brand_cat_list = []
            for cat in cat_class.all_cats:
                for word in brand_word_list:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        brand_cat_list.append(cat)

            name_cat_list = []
            name_cat_counts = {}
            for cat in cat_class.all_cats:
                for word in name_word_list:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        if cat not in name_cat_list:
                            name_cat_list.append(cat)
                            name_cat_counts[cat] = 1
                        else:
                            name_cat_counts[cat] += 1

            removable_cats = []
            for name_cat in name_cat_list:
                if name_cat in brand_cat_list and name_cat_counts[name_cat] == 1 and name_cat not in exceptions:
                    removable_cats.append(name_cat)
                    print(f'REMOVING: {name_cat}')

            if len(removable_cats) > 0:
                query_kind_cats = query_result.kind_cats
                query_pattern_cats = query_result.pattern_cats
                query_color_cats = query_result.color_cats
                query_style_cats = query_result.style_cats
                query_material_cats = query_result.material_cats
                query_attribute_cats = query_result.attribute_cats
                query_length_cats = query_result.length_cats
                query_filter_cats = query_result.filter_cats
                query_all_cats = query_result.all_cats

                for removable_cat in removable_cats:
                    if removable_cat in query_kind_cats:
                        query_kind_cats.remove(removable_cat)
                    if removable_cat in query_pattern_cats:
                        query_pattern_cats.remove(removable_cat)
                    if removable_cat in query_color_cats:
                        query_color_cats.remove(removable_cat)
                    if removable_cat in query_style_cats:
                        query_style_cats.remove(removable_cat)
                    if removable_cat in query_material_cats:
                        query_material_cats.remove(removable_cat)
                    if removable_cat in query_attribute_cats:
                        query_attribute_cats.remove(removable_cat)
                    if removable_cat in query_length_cats:
                        query_length_cats.remove(removable_cat)
                    if removable_cat in query_filter_cats:
                        query_filter_cats.remove(removable_cat)
                    if removable_cat in query_all_cats:
                        query_all_cats.remove(removable_cat)

                query_result.kind_cats = query_kind_cats
                query_result.pattern_cats = query_pattern_cats
                query_result.color_cats = query_color_cats
                query_result.style_cats = query_style_cats
                query_result.material_cats = query_material_cats
                query_result.attribute_cats = query_attribute_cats
                query_result.length_cats = query_length_cats
                query_result.filter_cats = query_filter_cats
                query_result.all_cats = query_all_cats

                db.session.commit()
            print('-------------------------------------------------')

        return True
    else:
        return False


def cat_fix_liu(db, ImagesSkinny, data):
    transform_key = os.environ['TRANSFORM_KEY']
    if data['transform_key'] == transform_key:
        img_hashes = db.session.query(
            ImagesSkinny.img_hash
        ).filter(
            ImagesSkinny.brand == 'LIU JO'
        ).order_by(func.random()).all()

        total_count = len(img_hashes)
        counter = 0
        for img_hash in img_hashes:
            query_result = ImagesSkinny.query.filter_by(img_hash=img_hash).first()
            query_name = query_result.name
            counter += 1
            print(f'line: {counter}')
            if query_name.count('JEANS') == 1:
                query_kind_cats = query_result.kind_cats
                query_all_cats = query_result.all_cats

                query_kind_cats.remove('jean')
                query_all_cats.remove('jean')

                query_result.kind_cats = query_kind_cats
                query_result.all_cats = query_all_cats

                db.session.commit()
                print(f'from: {total_count}')
                print(f'UPDATED: {query_name}')

        return True
    else:
        return False


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
