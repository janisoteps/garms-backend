# import os
from sqlalchemy import func
from datetime import datetime


def old_data_purge(db, ImagesSkinny, ImagesFull, Products):
    year_month_ok = [
        '2020-3',
        '2020-2'
    ]
    year_month_old = [
        '2019-3',
        '2019-4',
        '2019-5',
        '2019-7',
        '2019-12',
        '2020-1'
    ]
    all_prods = db.session.query(
        Products.prod_id,
        Products.date,
        Products.is_deleted
    ).filter(
        Products.is_deleted == None
    ).all()

    print(f'LENGTH: {len(all_prods)}')
    
    prod_counter_in = 0
    prod_counter_deleted = 0
    img_counter_deleted = 0

    for prod in all_prods:
        prod_counter_in += 1
        print(f'PRODS IN: {prod_counter_in}')
        year_month = f'{datetime.fromtimestamp(prod.date).year}-{datetime.fromtimestamp(prod.date).month}'
        if year_month in year_month_old:
            prod_result = Products.query.filter_by(prod_id=prod.prod_id).first()
            if prod_result.is_fav == False:
                prod_result.is_deleted = True
                db.session.commit()
                prod_counter_deleted += 1
                print(f'PRODS DELETED: {prod_counter_deleted}')

                img_skinny_results = ImagesSkinny.query.filter_by(prod_id=prod.prod_id).all()
                for img_skinny_result in img_skinny_results:
                    img_skinny_result.is_deleted = True
                    db.session.commit()

                img_full_results = ImagesFull.query.filter_by(prod_id=prod.prod_id).all()
                for img_full_result in img_full_results:
                    img_full_result.is_deleted = True
                    db.session.commit()
                    img_counter_deleted += 1
                    print(f'IMAGES DELETED: {img_counter_deleted}')

    return True


def count_faved_prods(db, Products):
    fav_count_agg = db.session.query(
            Products.is_fav,
            func.count(Products.is_fav)
        ).group_by(
            Products.is_fav
        ).all()

    return {
        'response': fav_count_agg
    }


def count_prod_dates(db, Products):
    all_dates = db.session.query(
        Products.date
    ).all()

    datetime_list = []
    for all_date in all_dates:
        datetime_list.append(all_date.date)

    year_month_list = list(map(
        lambda x: f'{datetime.fromtimestamp(x).year}-{datetime.fromtimestamp(x).month}',
        datetime_list
    ))
    year_month_tuples = [(x, 1) for x in year_month_list]
    count_dict = dict()
    for (date_string, val) in year_month_tuples:
        count_dict[date_string] = count_dict.get(date_string, 0) + val

    return count_dict


def count_deleted(db, Products):
    deleted_count_agg = db.session.query(
        Products.is_deleted,
        func.count(Products.is_deleted)
    ).group_by(
        Products.is_deleted
    ).all()

    return {
        'response': deleted_count_agg
    }