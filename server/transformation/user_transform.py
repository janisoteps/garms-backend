from hashlib import sha256


def add_user_hash(db, User):
    all_users = db.session.query(User).all()

    print(f'User count: {len(all_users)}')
    counter = 0
    for user in all_users:
        user_email = user.email
        hash_object = sha256(user_email.encode('utf8'))
        user.user_hash = hash_object.hexdigest()
        db.session.commit()
        counter += 1
        print(f'Users updated: {counter}')

    return True
