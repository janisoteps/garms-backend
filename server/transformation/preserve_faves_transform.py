import os
import json


# Iterate through all rows in Image db and recalculate kind, filter and all_cats columns
class PreserveFaves:
    def preserve_faves_transform(
            self,
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
            ).all()

            counter = 0
            for user in all_users:
                wardrobe = user.wardrobe
                if wardrobe is not None:
                    print(f'Preserving wardrobe of: {user.email}')

                    for wardrobe_product in wardrobe:
                        wardrobe_prod_id = wardrobe_product['prod_id']

                        img_result = db.session.query(ImagesV2).filter(
                            ImagesV2.prod_id == wardrobe_prod_id
                        ).first()

                        if img_result is not None:
                            img_submission = Images(
                                img_hash=img_result.img_hash,
                                img_url=img_result.img_url,
                                prod_id=img_result.prod_id,
                                prod_url=img_result.prod_url,
                                brand=img_result.brand,
                                color_string=img_result.color_string,
                                date=img_result.date,
                                name=img_result.name,
                                price=img_result.price,
                                sale=img_result.sale,
                                saleprice=img_result.saleprice,
                                discount_rate=0,
                                sex=img_result.sex,
                                shop=img_result.shop,
                                kind_cats=img_result.kind_cats,
                                pattern_cats=img_result.color_pattern_cats,
                                color_cats=img_result.color_pattern_cats,
                                style_cats=img_result.style_cats,
                                material_cats=img_result.material_cats,
                                attribute_cats=img_result.attribute_cats,
                                length_cats=[],
                                filter_cats=img_result.filter_cats,
                                all_cats=img_result.all_cats,
                                color_1=img_result.color_1,
                                color_1_hex=img_result.color_1_hex,
                                color_2=img_result.color_2,
                                color_2_hex=img_result.color_2_hex,
                                color_3=img_result.color_3,
                                color_3_hex=img_result.color_3_hex,
                                size_stock=img_result.size_stock,
                                in_stock=img_result.in_stock,
                                encoding_vgg16=img_result.encoding_vgg16
                            )

                            img_skinny_result = db.session.query(ImagesV2Skinny).filter(
                                ImagesV2Skinny.prod_id == wardrobe_prod_id
                            ).first()

                            img_skinny_submission = ImagesSkinny(
                                img_hash=img_skinny_result.img_hash,
                                img_url=img_skinny_result.img_url,
                                prod_id=img_skinny_result.prod_id,
                                prod_url=img_skinny_result.prod_url,
                                brand=img_skinny_result.brand,
                                color_string=img_skinny_result.color_string,
                                date=img_skinny_result.date,
                                name=img_skinny_result.name,
                                price=img_skinny_result.price,
                                sale=img_skinny_result.sale,
                                saleprice=img_skinny_result.saleprice,
                                discount_rate=img_skinny_result.discount_rate,
                                sex=img_skinny_result.sex,
                                shop=img_skinny_result.shop,
                                kind_cats=img_skinny_result.kind_cats,
                                pattern_cats=img_skinny_result.color_pattern_cats,
                                color_cats=img_skinny_result.color_pattern_cats,
                                style_cats=img_skinny_result.style_cats,
                                material_cats=img_skinny_result.material_cats,
                                attribute_cats=img_skinny_result.attribute_cats,
                                length_cats=[],
                                filter_cats=img_skinny_result.filter_cats,
                                all_cats=img_skinny_result.all_cats,
                                color_1=img_result.color_1,
                                color_2=img_result.color_2,
                                color_3=img_result.color_3,
                                size_stock=img_skinny_result.size_stock,
                                in_stock=img_skinny_result.in_stock
                            )

                            prod_result = db.session.query(ProductsV2).filter(
                                ProductsV2.prod_id == wardrobe_prod_id
                            ).first()

                            product_submission = Products(
                                prod_id=prod_result.prod_id,
                                name=prod_result.name,
                                prod_url=prod_result.prod_url,
                                brand=prod_result.brand,
                                category=prod_result.category,
                                color_string=prod_result.color_string,
                                currency=prod_result.currency,
                                date=prod_result.date,
                                description=prod_result.description,
                                image_hash=prod_result.image_hash,
                                image_urls=prod_result.image_urls,
                                price=prod_result.price,
                                sale=prod_result.sale,
                                saleprice=prod_result.saleprice,
                                discount_rate=img_skinny_result.discount_rate,
                                sex=prod_result.sex,
                                shop=prod_result.shop,
                                kind_cats=prod_result.kind_cats,
                                pattern_cats=prod_result.color_pattern_cats,
                                color_cats=prod_result.color_pattern_cats,
                                style_cats=prod_result.style_cats,
                                material_cats=prod_result.material_cats,
                                attribute_cats=prod_result.attribute_cats,
                                length_cats=[],
                                filter_cats=prod_result.filter_cats,
                                all_cats=prod_result.all_cats,
                                size_stock=img_skinny_result.size_stock,
                                in_stock=img_skinny_result.in_stock,
                                is_fav=prod_result.is_fav
                            )
    
                            try:
                                db.session.add(img_skinny_submission)
                                db.session.commit()
                            except:
                                db.session.rollback()
                                print('already there')

                            try:
                                db.session.add(img_submission)
                                db.session.commit()
                            except:
                                db.session.rollback()
                                print('already there')

                            try:
                                db.session.add(product_submission)
                                db.session.commit()
                            except:
                                db.session.rollback()
                                print('already there')

                            print(f'PROD PRESERVED: {img_skinny_result.name}')
                            counter += 1
                            print(f'{counter} PRODS')

            return json.dumps(True)
