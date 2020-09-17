import json


def image_commit(db, ImagesModel, SkinnyImagesModel, data):
    img_hash = data['img_hash']
    img_url = data['img_url']
    prod_id = data['prod_id']
    prod_url = data['prod_url']
    brand = data['brand']
    color_string = data['color_string']
    date = data['date']
    name = data['name']
    price = data['price']
    sale = data['sale']
    saleprice = data['saleprice']
    discount_rate = data['discount_rate']
    sex = data['sex']
    shop = data['shop']
    kind_cats = data['kind_cats']
    pattern_cats = data['pattern_cats']
    color_cats = data['color_cats']
    style_cats = data['style_cats']
    material_cats = data['material_cats']
    attribute_cats = data['attribute_cats']
    length_cats = data['length_cats']
    filter_cats = data['filter_cats']
    all_cats = data['all_cats']
    color_1 = data['color_1']
    color_1_hex = data['color_1_hex']
    color_2 = data['color_2']
    color_2_hex = data['color_2_hex']
    color_3 = data['color_3']
    color_3_hex = data['color_3_hex']
    color_4 = data['color_4']
    color_4_hex = data['color_4_hex']
    color_5 = data['color_5']
    color_5_hex = data['color_5_hex']
    color_6 = data['color_6']
    color_6_hex = data['color_6_hex']
    color_hist = data['color_hist']
    size_stock = data['size_stock']
    in_stock = data['in_stock']
    encoding_vgg16 = data['encoding_vgg16']
    is_deleted = False

    print(prod_url)
    img_full_submission = ImagesModel(
        img_hash=img_hash,
        img_url=img_url,
        prod_id=prod_id,
        prod_url=prod_url,
        brand=brand,
        color_string=color_string,
        date=date,
        date_updated=date,
        name=name,
        price=price,
        sale=sale,
        saleprice=saleprice,
        discount_rate=discount_rate,
        sex=sex,
        shop=shop,
        kind_cats=kind_cats,
        pattern_cats=pattern_cats,
        color_cats=color_cats,
        style_cats=style_cats,
        material_cats=material_cats,
        attribute_cats=attribute_cats,
        length_cats=length_cats,
        filter_cats=filter_cats,
        all_cats=all_cats,
        color_1=color_1,
        color_1_hex=color_1_hex,
        color_2=color_2,
        color_2_hex=color_2_hex,
        color_3=color_3,
        color_3_hex=color_3_hex,
        color_4=color_4,
        color_4_hex=color_4_hex,
        color_5=color_5,
        color_5_hex=color_5_hex,
        color_6=color_6,
        color_6_hex=color_6_hex,
        color_hist=color_hist,
        size_stock=size_stock,
        in_stock=in_stock,
        encoding_vgg16=encoding_vgg16,
        is_deleted=is_deleted
    )

    img_skinny_submission = SkinnyImagesModel(
        img_hash=img_hash,
        img_url=img_url,
        prod_id=prod_id,
        prod_url=prod_url,
        brand=brand,
        color_string=color_string,
        date=date,
        date_updated=date,
        name=name,
        price=price,
        sale=sale,
        saleprice=saleprice,
        discount_rate=discount_rate,
        sex=sex,
        shop=shop,
        kind_cats=kind_cats,
        pattern_cats=pattern_cats,
        color_cats=color_cats,
        style_cats=style_cats,
        material_cats=material_cats,
        attribute_cats=attribute_cats,
        length_cats=length_cats,
        filter_cats=filter_cats,
        all_cats=all_cats,
        color_1=color_1,
        color_2=color_2,
        color_3=color_3,
        color_4=color_4,
        color_5=color_5,
        color_6=color_6,
        size_stock=size_stock,
        in_stock=in_stock,
        is_deleted=is_deleted
    )

    try:
        existing_img_full_row = ImagesModel.query.filter_by(img_hash=img_hash).first()
        existing_img_skinny_row = SkinnyImagesModel.query.filter_by(img_hash=img_hash).first()
    except:
        existing_img_full_row = None
        existing_img_skinny_row = None

    if existing_img_full_row is None or existing_img_skinny_row is None:
        print('Adding new IMG rows')
        db.session.add(img_skinny_submission)
        db.session.commit()
        db.session.add(img_full_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('Image ALREADY IN DB')

        existing_img_full_row.prod_id = prod_id
        existing_img_full_row.prod_url = prod_url
        existing_img_full_row.brand = brand
        existing_img_full_row.color_string = color_string
        existing_img_full_row.date_updated = date
        existing_img_full_row.name = name
        existing_img_full_row.price = price
        existing_img_full_row.sale = sale
        existing_img_full_row.saleprice = saleprice
        existing_img_full_row.discount_rate = discount_rate
        existing_img_full_row.kind_cats = kind_cats
        existing_img_full_row.pattern_cats = pattern_cats
        existing_img_full_row.color_cats = color_cats
        existing_img_full_row.style_cats = style_cats
        existing_img_full_row.material_cats = material_cats
        existing_img_full_row.attribute_cats = attribute_cats
        existing_img_full_row.length_cats = length_cats
        existing_img_full_row.filter_cats = filter_cats
        existing_img_full_row.all_cats = all_cats
        existing_img_full_row.color_1 = color_1
        existing_img_full_row.color_1_hex = color_1_hex
        existing_img_full_row.color_2 = color_2
        existing_img_full_row.color_2_hex = color_2_hex
        existing_img_full_row.color_3 = color_3
        existing_img_full_row.color_3_hex = color_3_hex
        existing_img_full_row.color_4 = color_4
        existing_img_full_row.color_4_hex = color_4_hex
        existing_img_full_row.color_5 = color_5
        existing_img_full_row.color_5_hex = color_5_hex
        existing_img_full_row.color_6 = color_6
        existing_img_full_row.color_6_hex = color_6_hex
        existing_img_full_row.color_hist = color_hist
        existing_img_full_row.encoding_vgg16 = encoding_vgg16
        existing_img_full_row.size_stock = size_stock
        existing_img_full_row.in_stock = in_stock
        existing_img_full_row.is_deleted = is_deleted

        existing_img_skinny_row.prod_id = prod_id
        existing_img_skinny_row.prod_url = prod_url
        existing_img_skinny_row.brand = brand
        existing_img_skinny_row.color_string = color_string
        existing_img_skinny_row.date_updated = date
        existing_img_skinny_row.name = name
        existing_img_skinny_row.price = price
        existing_img_skinny_row.sale = sale
        existing_img_skinny_row.saleprice = saleprice
        existing_img_skinny_row.discount_rate = discount_rate
        existing_img_skinny_row.kind_cats = kind_cats
        existing_img_skinny_row.pattern_cats = pattern_cats
        existing_img_skinny_row.color_cats = color_cats
        existing_img_skinny_row.style_cats = style_cats
        existing_img_skinny_row.material_cats = material_cats
        existing_img_skinny_row.attribute_cats = attribute_cats
        existing_img_skinny_row.length_cats = length_cats
        existing_img_skinny_row.filter_cats = filter_cats
        existing_img_skinny_row.all_cats = all_cats
        existing_img_skinny_row.color_1 = color_1
        existing_img_skinny_row.color_2 = color_2
        existing_img_skinny_row.color_3 = color_3
        existing_img_skinny_row.color_4 = color_4
        existing_img_skinny_row.color_5 = color_5
        existing_img_skinny_row.color_6 = color_6
        existing_img_skinny_row.size_stock = size_stock
        existing_img_skinny_row.in_stock = in_stock
        existing_img_skinny_row.is_deleted = is_deleted

        db.session.commit()

        return json.dumps(True)


def product_commit(db, ProductModel, data):
    prod_id = data['prod_id']
    name = data['name']
    prod_url = data['prod_url']
    brand = data['brand']
    category = data['category']
    color_string = data['color_string']
    currency = data['currency']
    date = data['date']
    description = data['description']
    image_hash = data['image_hash']
    image_urls = data['image_urls']
    price = data['price']
    sale = data['sale']
    saleprice = data['saleprice']
    discount_rate = data['discount_rate']
    sex = data['sex']
    shop = data['shop']
    kind_cats = data['kind_cats']
    pattern_cats = data['pattern_cats']
    color_cats = data['color_cats']
    style_cats = data['style_cats']
    material_cats = data['material_cats']
    attribute_cats = data['attribute_cats']
    length_cats = data['length_cats']
    filter_cats = data['filter_cats']
    all_cats = data['all_cats']
    size_stock = data['size_stock']
    in_stock = data['in_stock']
    is_fav = False
    is_deleted = False
    is_old = False

    product_submission = ProductModel(
        prod_id=prod_id,
        name=name,
        prod_url=prod_url,
        brand=brand,
        category=category,
        color_string=color_string,
        currency=currency,
        date=date,
        date_updated=date,
        description=description,
        image_hash=image_hash,
        image_urls=image_urls,
        price=price,
        sale=sale,
        saleprice=saleprice,
        discount_rate=discount_rate,
        sex=sex,
        shop=shop,
        kind_cats=kind_cats,
        pattern_cats=pattern_cats,
        color_cats=color_cats,
        style_cats=style_cats,
        material_cats=material_cats,
        attribute_cats=attribute_cats,
        length_cats=length_cats,
        filter_cats=filter_cats,
        all_cats=all_cats,
        size_stock=size_stock,
        in_stock=in_stock,
        is_fav=is_fav,
        is_deleted=is_deleted,
        is_old=is_old
    )

    try:
        existing_product = ProductModel.query.filter_by(prod_id=prod_id).first()
    except:
        existing_product = None

    if existing_product is None:
        print('Adding a new product')
        db.session.add(product_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('PRODUCT ALREADY EXISTS')

        existing_product.name = name
        existing_product.category = category
        existing_product.color_string = color_string
        existing_product.currency = currency
        existing_product.date_updated = date
        existing_product.description = description
        existing_product.image_hash = image_hash
        existing_product.image_urls = image_urls
        existing_product.price = price
        existing_product.sale = sale
        existing_product.saleprice = saleprice
        existing_product.discount_rate = discount_rate
        existing_product.size_stock = size_stock
        existing_product.kind_cats = kind_cats
        existing_product.pattern_cats = pattern_cats
        existing_product.color_cats = color_cats
        existing_product.style_cats = style_cats
        existing_product.material_cats = material_cats
        existing_product.attribute_cats = attribute_cats
        existing_product.length_cats = length_cats
        existing_product.filter_cats = filter_cats
        existing_product.all_cats = all_cats
        existing_product.size_stock = size_stock
        existing_product.in_stock = in_stock
        existing_product.is_deleted = is_deleted
        is_old.is_deleted = is_old

        db.session.commit()

        return json.dumps(True)


def insta_mention_commit(db, InstaMentions, data):
    print(data)
    mention_username = data['mention_username']
    comment_id = data['comment_id']
    mention_timestamp = data['mention_timestamp']
    media_id = data['media_id']
    media_type = data['media_type']
    media_url = data['media_url']
    media_permalink = data['media_permalink']
    owner_username = data['owner_username']

    insta_submission = InstaMentions(
        mention_username=mention_username,
        comment_id=comment_id,
        mention_timestamp=mention_timestamp,
        media_id=media_id,
        media_type=media_type,
        media_url=media_url,
        media_permalink=media_permalink,
        owner_username=owner_username
    )

    try:
        existing_mention = InstaMentions.query.filter_by(comment_id=comment_id).first()
    except:
        existing_mention = None

    if existing_mention is None:
        db.session.add(insta_submission)
        db.session.commit()

    return json.dumps(True)
