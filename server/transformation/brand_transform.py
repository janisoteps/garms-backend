import os
# from sqlalchemy import func


# Iterate through all rows in Image db and recalculate kind, filter and all_cats columns
class BrandTransform:
    def add_brand_to_images(self, db, ImagesV2, ProductsV2, data):
        key_string = os.environ['TRANSFORM_KEY']
        if data['transform_key'] == key_string:

            img_hashes = db.session.query(
                ImagesV2.img_hash
            ).all()

            counter = 0
            for img_hash in img_hashes:
                counter += 1
                print(f'count : {counter}')

                prod_result = db.session.query(
                    ProductsV2.image_hash,
                    ProductsV2.brand
                ).filter(ProductsV2.image_hash.any(img_hash)).first()

                if prod_result is not None:
                    db.session.query(ImagesV2).filter(ImagesV2.img_hash == img_hash).update({'brand': prod_result.brand})

                    db.session.commit()

        return True
