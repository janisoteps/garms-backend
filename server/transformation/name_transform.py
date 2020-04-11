import os
from sqlalchemy import func


class NameTransform:
    def prod_name_fix(self, data, db, ImagesSkinny, Products):
        key_string = os.environ['TRANSFORM_KEY']
        if data['transform_key'] == key_string:
            prod_ids = db.session.query(
                Products.prod_id
            ).filter(
                Products.name == None,
                Products.is_deleted is not True
            ).order_by(func.random()).all()

            total_prods = len(prod_ids)
            print(f'total len: {total_prods}')
            counter = 0
            failed_counter = 0
            for prod_id in prod_ids:
                img_result = ImagesSkinny.query.filter_by(prod_id=prod_id).first()
                if img_result is not None:
                    img_name = img_result.name
                    db.session.query(Products).filter(Products.prod_id == prod_id).update({'name': img_name})
                    db.session.commit()
                    counter += 1
                    print(f'PRODS UPDATED: {counter}')
                    print(f'FAILED: {failed_counter}')
                    print(f'TOTAL: {total_prods}')

                else:
                    db.session.query(Products).filter(Products.prod_id == prod_id).update({'is_deleted': True})
                    db.session.commit()
                    failed_counter += 1
                    print(f'PRODS UPDATED: {counter}')
                    print(f'FAILED: {failed_counter}')
                    print(f'TOTAL: {total_prods}')

        return True
