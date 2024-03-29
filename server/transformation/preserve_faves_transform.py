import os
import json
import time


def preserve_faves_transform(
        db,
        Images,
        ImagesV2,
        ImagesSkinny,
        ImagesV2Skinny,
        Products,
        ProductsV2,
        User,
        data
):
    key_string = os.environ['TRANSFORM_KEY']
    if data['transform_key'] == key_string:
        all_users = db.session.query(
            User
        ).filter(
            User.sex == data['sex']
        ).all()

        counter = 0
        user_counter = 0
        for user in all_users:
            user_counter += 1
            print(f'USER NR: {user_counter}')
            wardrobe = user.wardrobe
            if wardrobe is not None:
                print(f'Preserving wardrobe of: {user.email}')

                for wardrobe_product in wardrobe:
                    wardrobe_prod_id = wardrobe_product['prod_id']

                    prod_result = db.session.query(ProductsV2).filter(
                        ProductsV2.prod_id == wardrobe_prod_id
                    ).first()

                    img_results = db.session.query(ImagesV2).filter(
                        ImagesV2.prod_id == wardrobe_prod_id
                    ).all()

                    if img_results is not None:
                        for img_result in img_results:

                            img_skinny_submission = ImagesSkinny(
                                img_hash=img_result.img_hash,
                                img_url=img_result.img_url,
                                prod_id=img_result.prod_id,
                                prod_url=img_result.prod_url,
                                brand=img_result.brand,
                                color_string=img_result.color_string,
                                date=img_result.date,
                                date_updated=img_result.date_updated,
                                name=img_result.name,
                                price=img_result.price,
                                sale=img_result.sale,
                                saleprice=img_result.saleprice,
                                discount_rate=img_result.discount_rate,
                                sex=img_result.sex,
                                shop=img_result.shop,
                                kind_cats=img_result.kind_cats,
                                pattern_cats=img_result.pattern_cats,
                                color_cats=img_result.color_cats,
                                style_cats=img_result.style_cats,
                                material_cats=img_result.material_cats,
                                attribute_cats=img_result.attribute_cats,
                                length_cats=img_result.length_cats,
                                filter_cats=img_result.filter_cats,
                                all_cats=img_result.all_cats,
                                color_1=img_result.color_1,
                                color_2=img_result.color_2,
                                color_3=img_result.color_3,
                                color_4=img_result.color_4,
                                color_5=img_result.color_5,
                                color_6=img_result.color_6,
                                size_stock=img_result.size_stock,
                                in_stock=img_result.in_stock,
                                is_deleted=False
                            )

                            img_submission = Images(
                                img_hash=img_result.img_hash,
                                img_url=img_result.img_url,
                                prod_id=img_result.prod_id,
                                prod_url=img_result.prod_url,
                                brand=img_result.brand,
                                color_string=img_result.color_string,
                                date=img_result.date,
                                date_updated=img_result.date_updated,
                                name=img_result.name,
                                price=img_result.price,
                                sale=img_result.sale,
                                saleprice=img_result.saleprice,
                                discount_rate=img_result.discount_rate,
                                sex=img_result.sex,
                                shop=img_result.shop,
                                kind_cats=img_result.kind_cats,
                                pattern_cats=img_result.pattern_cats,
                                color_cats=img_result.color_cats,
                                style_cats=img_result.style_cats,
                                material_cats=img_result.material_cats,
                                attribute_cats=img_result.attribute_cats,
                                length_cats=img_result.length_cats,
                                filter_cats=img_result.filter_cats,
                                all_cats=img_result.all_cats,
                                color_1=img_result.color_1,
                                color_1_hex=img_result.color_1_hex,
                                color_2=img_result.color_2,
                                color_2_hex=img_result.color_2_hex,
                                color_3=img_result.color_3,
                                color_3_hex=img_result.color_3_hex,
                                color_4=img_result.color_4,
                                color_4_hex=img_result.color_4_hex,
                                color_5=img_result.color_5,
                                color_5_hex=img_result.color_5_hex,
                                color_6=img_result.color_6,
                                color_6_hex=img_result.color_6_hex,
                                color_hist=None,
                                size_stock=img_result.size_stock,
                                in_stock=img_result.in_stock,
                                encoding_vgg16=img_result.encoding_vgg16,
                                is_deleted=False
                            )

                            product_submission = Products(
                                prod_id=prod_result.prod_id,
                                name=prod_result.name,
                                prod_url=prod_result.prod_url,
                                brand=prod_result.brand,
                                category=prod_result.category,
                                color_string=prod_result.color_string,
                                currency=prod_result.currency,
                                date=prod_result.date,
                                date_updated=prod_result.date_updated,
                                description=prod_result.description,
                                image_hash=prod_result.image_hash,
                                image_urls=prod_result.image_urls,
                                price=prod_result.price,
                                sale=prod_result.sale,
                                saleprice=prod_result.saleprice,
                                discount_rate=prod_result.discount_rate,
                                sex=prod_result.sex,
                                shop=prod_result.shop,
                                kind_cats=prod_result.kind_cats,
                                pattern_cats=prod_result.pattern_cats,
                                color_cats=prod_result.color_cats,
                                style_cats=prod_result.style_cats,
                                material_cats=prod_result.material_cats,
                                attribute_cats=prod_result.attribute_cats,
                                length_cats=prod_result.length_cats,
                                filter_cats=prod_result.filter_cats,
                                all_cats=prod_result.all_cats,
                                size_stock=img_result.size_stock,
                                in_stock=img_result.in_stock,
                                is_fav=prod_result.is_fav,
                                is_deleted=False,
                                is_old=True
                            )

                            existing_skinny_rows = db.session.query(ImagesSkinny).filter(
                                ImagesSkinny.img_hash == img_result.img_hash
                            ).all()
                            if len(existing_skinny_rows) == 0:
                                print(f'add skinny: {img_result.img_hash}')
                                db.session.add(img_skinny_submission)
                                db.session.commit()

                            existing_img_rows = db.session.query(Images).filter(
                                Images.img_hash == img_result.img_hash
                            ).all()
                            if len(existing_img_rows) == 0:
                                print(f'add image: {img_result.img_hash}')
                                db.session.add(img_submission)
                                db.session.commit()

                            existing_prod = db.session.query(Products).filter(
                                Products.prod_id == wardrobe_prod_id
                            ).first()
                            if existing_prod is None:
                                print(f'add prod: {prod_result.prod_id}')
                                db.session.add(product_submission)
                                db.session.commit()
                            else:
                                existing_prod.is_old = True
                                db.session.commit()

                            print(f'PROD PRESERVED: {img_result.name}')
                            counter += 1
                            print(f'{counter} PRODS')

        return json.dumps(True)


def get_fav_images(db, Products, data):
    key_string = os.environ['TRANSFORM_KEY']
    if data['transform_key'] == key_string:
        faved_prods = db.session.query(
            Products
        ).filter(
            Products.is_fav == True
        ).all()

        img_hash_list = []
        for faved_prod in faved_prods:
            img_hashes = faved_prod.image_hash
            for img_hash in img_hashes:
                img_hash_list.append(img_hash)

        return img_hash_list


def get_img_data(db, ImagesFull, ImagesFullSchema, data):
    key_string = os.environ['TRANSFORM_KEY']
    if data['transform_key'] == key_string:
        img_query_result = db.session.query(
            ImagesFull
        ).filter(
            ImagesFull.img_hash == data['img_hash']
        ).first()

        img_serial = ImagesFullSchema().dump(img_query_result)
        result_dict = {
            'image_data': img_serial[0]
        }
        return result_dict


# def update_img_enc(db, ImagesFull, data):
#     key_string = os.environ['TRANSFORM_KEY']
#     if data['transform_key'] == key_string:
#         img_query_result = db.session.query(
#             ImagesFull
#         ).filter(
#             ImagesFull.img_hash == data['img_hash']
#         ).first()
#
#         img_query_result.encoding_vgg16 = data['encoding_vgg16']
#         db.session.commit()
#
#         return json.dumps(True)
