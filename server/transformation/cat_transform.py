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
                        new_kind_cats = [cat for cat in query_kind_cats if cat != removable_cat]
                        query_result.kind_cats = new_kind_cats

                    if removable_cat in query_pattern_cats:
                        new_pattern_cats = [cat for cat in query_pattern_cats if cat != removable_cat]
                        query_result.pattern_cats = new_pattern_cats

                    if removable_cat in query_color_cats:
                        new_color_cats = [cat for cat in query_color_cats if cat != removable_cat]
                        query_result.color_cats = new_color_cats

                    if removable_cat in query_style_cats:
                        new_style_cats = [cat for cat in query_style_cats if cat != removable_cat]
                        query_result.style_cats = new_style_cats

                    if removable_cat in query_material_cats:
                        new_material_cats = [cat for cat in query_material_cats if cat != removable_cat]
                        query_result.material_cats = new_material_cats

                    if removable_cat in query_attribute_cats:
                        new_attribute_cats = [cat for cat in query_attribute_cats if cat != removable_cat]
                        query_result.attribute_cats = new_attribute_cats

                    if removable_cat in query_length_cats:
                        new_length_cats = [cat for cat in query_length_cats if cat != removable_cat]
                        query_result.length_cats = new_length_cats

                    if removable_cat in query_filter_cats:
                        new_filter_cats = [cat for cat in query_filter_cats if cat != removable_cat]
                        query_result.filter_cats = new_filter_cats

                    if removable_cat in query_all_cats:
                        new_all_cats = [cat for cat in query_all_cats if cat != removable_cat]
                        query_result.all_cats = new_all_cats

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

                new_kind_cats = [cat for cat in query_kind_cats if cat != 'jean']
                new_all_cats = [cat for cat in query_all_cats if cat != 'jean']

                query_result.kind_cats = new_kind_cats
                query_result.all_cats = new_all_cats

                db.session.commit()
                print(f'from: {total_count}')
                print(f'UPDATED: {query_name}')

        return True
    else:
        return False


def cat_fix_boohoo(db, ImagesSkinny, data, cats):
    cat_list = cats.Cats()
    kind_cats = cat_list.kind_cats
    pattern_cats = cat_list.pattern_cats
    color_cats = cat_list.color_cats
    style_cats = cat_list.style_cats
    material_cats = cat_list.material_cats
    attribute_cats = cat_list.attribute_cats
    length_cats = cat_list.length_cats
    filter_cats = cat_list.filter_cats

    transform_key = os.environ['TRANSFORM_KEY']
    if data['transform_key'] == transform_key:
        img_hashes = db.session.query(
            ImagesSkinny.img_hash
        ).filter(
            ImagesSkinny.shop == 'Boohoo'
        ).order_by(func.random()).all()

        total_count = len(img_hashes)
        counter = 0
        for img_hash in img_hashes:
            query_result = ImagesSkinny.query.filter_by(img_hash=img_hash).first()
            query_name = query_result.name
            name_arr = query_name.lower().split(' ')
            cat_name_arr = [word.replace('*', '') for word in name_arr]

            new_kind_cats = []
            new_pattern_cats = []
            new_color_cats = []
            new_style_cats = []
            new_material_cats = []
            new_attribute_cats = []
            new_length_cats = []
            new_filter_cats = []
            new_all_cats = []

            for cat in kind_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_kind_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in pattern_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_pattern_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in color_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_color_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in style_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_style_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in material_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_material_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in attribute_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_attribute_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in length_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_length_cats.append(cat)
                        new_all_cats.append(cat)
            for cat in filter_cats:
                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_filter_cats.append(cat)
                        new_all_cats.append(cat)

            query_result.kind_cats = new_kind_cats
            query_result.pattern_cats = new_pattern_cats
            query_result.color_cats = new_color_cats
            query_result.style_cats = new_style_cats
            query_result.material_cats = new_material_cats
            query_result.attribute_cats = new_attribute_cats
            query_result.length_cats = new_length_cats
            query_result.filter_cats = new_filter_cats
            query_result.all_cats = new_all_cats

            db.session.commit()
            counter += 1
            print(f'count : {counter}')
            print(f'from: {total_count}')
            print(f'shop: {query_result.shop}')
            print(f'UPDATED: {query_name}')
            print('-------------------------------------------------\n')

        return True
    else:
        return False


def add_borg_cat(db, ImagesSkinny, data):
    transform_key = os.environ['TRANSFORM_KEY']
    cat = 'borg'
    if data['transform_key'] == transform_key:
        img_hashes = db.session.query(
            ImagesSkinny.img_hash
        ).order_by(func.random()).all()

        counter_in = 0
        counter_out = 0
        for img_hash in img_hashes:
            counter_in += 1
            print(f'LINES IN: {counter_in}')
            query_result = ImagesSkinny.query.filter_by(img_hash=img_hash).first()
            query_name = query_result.name

            if 'borg' in query_name:
                name_arr = query_name.lower().split(' ')
                cat_name_arr = [word.replace('*', '') for word in name_arr]

                query_material_cats = query_result.material_cats
                query_all_cats = query_result.all_cats
                new_material_cats = query_material_cats
                new_all_cats = query_all_cats

                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_material_cats.append(cat)
                        new_all_cats.append(cat)

                query_result.material_cats = new_material_cats
                query_result.all_cats = new_all_cats

                db.session.commit()
                counter_out += 1
                print(f'LINES OUT: {counter_out}')


def add_sweatpant_cat(db, ImagesSkinny, data):
    transform_key = os.environ['TRANSFORM_KEY']
    cat = 'sweatpants'
    if data['transform_key'] == transform_key:
        img_hashes = db.session.query(
            ImagesSkinny.img_hash
        ).order_by(func.random()).all()

        counter_in = 0
        counter_out = 0
        for img_hash in img_hashes:
            counter_in += 1
            if counter_in % 100 == 0:
                print(f'LINES IN: {counter_in}')
                print(f'LINES OUT: {counter_out}')
            query_result = ImagesSkinny.query.filter_by(img_hash=img_hash).first()
            query_name = query_result.name

            if 'sweatpants' in query_name:
                name_arr = query_name.lower().split(' ')
                cat_name_arr = [word.replace('*', '') for word in name_arr]

                query_kind_cats = query_result.kind_cats
                query_all_cats = query_result.all_cats
                new_kind_cats = query_kind_cats
                new_all_cats = query_all_cats

                for word in cat_name_arr:
                    if cat == word or f'{cat}s' == word or f'{cat}es' == word or f'{cat}ed' == word:
                        new_kind_cats.append(cat)
                        new_all_cats.append(cat)

                query_result.kind_cats = new_kind_cats
                query_result.all_cats = new_all_cats

                db.session.commit()
                counter_out += 1
                print(f'LINES OUT: {counter_out}')


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
