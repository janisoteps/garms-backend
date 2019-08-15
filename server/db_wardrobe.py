import json
import time


def db_add_look(db, User, data):
    email = data['email']
    look_name = data['look_name']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'
    user_looks = user_data.wardrobe
    if user_looks is not None:
        look_exists = look_name in user_looks
        if look_exists:
            return 'Look already exists'
        else:
            user_looks[look_name] = []
    else:
        user_looks = {look_name: []}

    user_data.wardrobe = user_looks
    db.session.commit()
    return json.dumps(user_data.wardrobe)


def db_remove_look(db, User, data):
    email = data['email']
    look_name = data['look_name']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'
    user_looks = user_data.wardrobe
    look_exists = look_name in user_looks
    if look_exists:
        user_looks.pop(look_name, None)
        user_data.wardrobe = user_looks
        db.session.commit()
        return json.dumps(user_looks)
    else:
        return 'Look not found'


def db_get_looks(db, User, data):
    email = data['email']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'

    user_looks = user_data.wardrobe
    return json.dumps(user_looks)


def db_add_outfit(db, User, data):
    email = data['email']
    look_name = data['look_name']
    prod_id = data['prod_id']

    user_data = User.query.filter_by(email=email).first()
    if user_data is None:
        return 'Invalid user email'

    user_looks = user_data.wardrobe
    if look_name in user_looks:
        outfit_arr = user_looks[look_name]
        user_data.wardrobe.pop(look_name)
        db.session.commit()

        outfit_arr.append({
            'prod_id': prod_id,
            'outfit_date': int(time.time())
        })
        user_data.wardrobe[look_name] = outfit_arr
        db.session.commit()
        return json.dumps(user_data.wardrobe)
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

    user_looks = user_data.wardrobe
    if look_name in user_looks:
        outfit_arr = user_looks[look_name]
        del_outfit = list(filter(lambda outfit: outfit['prod_id'] == prod_id and outfit['outfit_date'] == outfit_date, outfit_arr))
        if len(del_outfit) > 0:
            user_data.wardrobe.pop(look_name)
            db.session.commit()

            outfit_arr.remove(del_outfit[0])
            user_data.wardrobe[look_name] = outfit_arr
            db.session.commit()
            return json.dumps(user_data.wardrobe)
        else:
            return 'Outfit not found'
    else:
        return 'Invalid look'
