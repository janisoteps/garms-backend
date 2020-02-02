import json
import time


def db_add_look(db, User, data):
    email = data['email']
    look_name = data['look_name']
    look_date = int(time.time())

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'
    user_looks = user_data.looks
    if user_looks is not None:
        look_exists = any(d['look_name'] == look_name for d in user_looks)
        if look_exists:
            return 'Look already exists'
        else:
            user_looks.append({
                'look_date': look_date,
                'look_name': look_name
            })
    else:
        user_looks = [{
                'look_date': look_date,
                'look_name': look_name
            }]

    user_data.looks = user_looks
    db.session.commit()
    return json.dumps({
        'looks': user_data.looks,
        'wardrobe': user_data.wardrobe
    })


def db_remove_look(db, User, data):
    email = data['email']
    look_name = data['look_name']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'
    user_looks = user_data.looks
    user_outfits = user_data.wardrobe
    look_exists = any(d['look_name'] == look_name for d in user_looks)
    if look_exists:
        del_look = list(filter(lambda look: look['look_name'] == look_name, user_looks))
        del_outfits = list(filter(lambda outfit: outfit['look_name'] == look_name, user_outfits))
        user_looks.remove(del_look[0])
        for del_outfit in del_outfits:
            user_outfits.remove(del_outfit)
        user_data.looks = user_looks
        user_data.wardrobe = user_outfits
        db.session.commit()
        return json.dumps({
            'looks': user_data.looks,
            'wardrobe': user_data.wardrobe
        })
    else:
        return 'Look not found'


def db_get_looks(db, User, data):
    print('get looks called')
    email = data['email']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'

    if user_data.wardrobe is not None:
        res_wardrobe = [outfit for outfit in user_data.wardrobe if outfit['prod_id'] is not None]
    else:
        res_wardrobe = None

    return json.dumps({
            'looks': user_data.looks,
            'wardrobe': res_wardrobe
        })


def db_add_outfit(db, User, ProductsV2, data):
    email = data['email']
    look_name = data['look_name']
    # print(data)
    prod_id = data['prod_id']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'

    user_outfits = user_data.wardrobe
    if any(d['look_name'] == look_name for d in user_data.looks):
        if user_outfits is None:
            user_outfits = [{
                'prod_id': prod_id,
                'outfit_date': int(time.time()),
                'look_name': look_name
            }]
            user_data.wardrobe = user_outfits
            db.session.commit()
        else:
            user_outfits.append({
                'prod_id': prod_id,
                'outfit_date': int(time.time()),
                'look_name': look_name
            })
            user_data.wardrobe = user_outfits
            db.session.commit()

        added_prod = ProductsV2.query.filter_by(prod_id=prod_id).first()
        added_prod.is_fav = True
        db.session.commit()

        return json.dumps({
            'looks': user_data.looks,
            'wardrobe': user_data.wardrobe
        })
    else:
        return 'Invalid look'


def db_remove_outfit(db, User, data):
    email = data['email']
    look_name = data['look_name']
    prod_id = data['prod_id']
    outfit_date = data['outfit_date']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'

    user_outfits = user_data.wardrobe
    if any(d['look_name'] == look_name for d in user_data.looks):
        del_outfit = list(filter(lambda outfit: outfit['prod_id'] == prod_id and outfit['outfit_date'] == outfit_date, user_outfits))
        if len(del_outfit) > 0:
            user_outfits.remove(del_outfit[0])
            user_data.wardrobe = user_outfits
            db.session.commit()

            user_response_data = User.query.filter_by(email=email).first()
            if user_response_data.wardrobe is not None:
                res_wardrobe = [outfit for outfit in user_response_data.wardrobe if outfit['prod_id'] is not None]
            else:
                res_wardrobe = None
            return json.dumps({
                'looks': user_response_data.looks,
                'wardrobe': res_wardrobe
            })
        else:
            return 'Outfit not found'
    else:
        return 'Invalid look'


def db_rename_look(db, User, data):
    email = data['email']
    look_name = data['look_name']
    new_look_name = data['new_look_name']

    print(look_name)

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'
    user_looks = user_data.looks
    user_outfits = user_data.wardrobe
    look_exists = any(d['look_name'] == look_name for d in user_looks)
    if look_exists:
        update_look = list(filter(lambda look: look['look_name'] == look_name, user_looks))
        update_outfits = list(filter(lambda outfit: outfit['look_name'] == look_name, user_outfits))
        user_looks.remove(update_look[0])
        for del_outfit in update_outfits:
            user_outfits.remove(del_outfit)

        new_look = [{
            'look_date': u_look['look_date'],
            'look_name': new_look_name
        } for u_look in update_look]
        new_outfits = [{
            'prod_id': u_outfit['prod_id'],
            'look_name': new_look_name,
            'outfit_date': u_outfit['outfit_date']
        } for u_outfit in update_outfits]

        user_looks += new_look
        user_outfits += new_outfits

        user_data.looks = user_looks
        user_data.wardrobe = user_outfits
        db.session.commit()
        return json.dumps({
            'looks': user_data.looks,
            'wardrobe': user_data.wardrobe
        })
    else:
        return json.dumps('Look not found')
