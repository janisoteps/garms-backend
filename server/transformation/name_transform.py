import os


class NameTransform:
    def prod_name_fix(self, data, db, ImagesSkinny, Products):
        key_string = os.environ['TRANSFORM_KEY']
        if data['transform_key'] == key_string:
            prod_ids = db.session.query(
                Products.prod_id
            ).all()

            total_prods = len(prod_ids)
            counter = 0
            for prod_id in prod_ids:
                img_result = ImagesSkinny.query.filter_by(prod_id=prod_id).first()
                img_name = img_result.name

                if img_name is not None:
                    db.session.query(Products).filter(Products.prod_id == prod_id).update({'name': img_name})
                    db.session.commit()
                    counter += 1
                    print(f'PRODS UPDATED: {counter}')
                    print(f'TOTAL: {total_prods}')

        return True
