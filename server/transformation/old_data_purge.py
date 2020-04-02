# import os
from sqlalchemy import func
from datetime import datetime


def old_data_purge(db, ImagesSkinny, ImagesFull, Products, data):

    return False


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

