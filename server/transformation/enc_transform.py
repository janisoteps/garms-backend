import os
# from sqlalchemy import func


# Iterate through all rows in Image db and recalculate kind, filter and all_cats columns
class EncTransform:
    def enc_dim_transform(self, db, ImagesV2, data):
        key_string = os.environ['TRANSFORM_KEY']
        if data['transform_key'] == key_string:
            shop = data['shop']

            img_hashes = db.session.query(
                ImagesV2.img_hash
            ).filter(
                ImagesV2.shop == shop
            ).all()

            counter = 0
            for img_hash in img_hashes:
                counter += 1
                print(f'count : {counter}')
                query_result = ImagesV2.query.filter_by(img_hash=img_hash).first()

                correct_enc_arr = query_result.encoding_crop[0]
                query_result.encoding_crop = correct_enc_arr

                db.session.commit()

        return True
