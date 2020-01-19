import os
import json
# from sqlalchemy import func


# Iterate through all rows in Image db and recalculate kind, filter and all_cats columns
class SkinnyTransform:
    def img_skinny_transform(self, db, ImagesV2, ImagesV2Skinny, image_commit_v2_skinny, data):
        key_string = os.environ['TRANSFORM_KEY']
        if data['transform_key'] == key_string:

            img_hashes = db.session.query(
                ImagesV2.img_hash
            ).all()

            counter = 0
            for img_hash in img_hashes:
                counter += 1
                print(f'count : {counter}')
                query_result = ImagesV2.query.filter_by(img_hash=img_hash).first()

                discount_rate = 0
                if query_result.sale == True:
                    discount_rate = (query_result.price - query_result.saleprice) / query_result.price

                commit_dict = {
                    'img_hash': query_result.img_hash,
                    'img_url': query_result.img_url,
                    'prod_id': query_result.prod_id,
                    'prod_url': query_result.prod_url,
                    'brand': query_result.brand,
                    'color_string': query_result.color_string,
                    'date':  query_result.date,
                    'name': query_result.name,
                    'price': query_result.price,
                    'sale': query_result.sale,
                    'saleprice': query_result.saleprice,
                    'discount_rate': discount_rate,
                    'sex': query_result.sex,
                    'shop': query_result.shop,
                    'kind_cats': query_result.kind_cats,
                    'color_pattern_cats': query_result.color_pattern_cats,
                    'style_cats': query_result.style_cats,
                    'material_cats': query_result.material_cats,
                    'attribute_cats': query_result.attribute_cats,
                    'filter_cats': query_result.filter_cats,
                    'all_cats': query_result.all_cats,
                    'size_stock': query_result.size_stock,
                    'in_stock': query_result.in_stock
                }

                image_commit_v2_skinny(db, ImagesV2Skinny, commit_dict)
                print(f'COMITTED: {query_result.mg_url}')

        return json.dumps(True)
