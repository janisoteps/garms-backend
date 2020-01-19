import json


def image_commit(db, Images, data):

    img_hash = data['img_hash']
    prod_url = data['prod_url']
    img_url = data['img_url']
    name = data['name']
    description = data['description']
    brand = data['brand']
    shop = data['shop']
    date = data['date']
    sex = data['sex']
    currency = data['currency']
    price = data['price']
    sale = data['sale']
    saleprice = data['saleprice']
    spider_cat = data['spider_cat']
    img_cats_ai_txt = data['img_cats_ai_txt']
    img_cats_sc_txt = data['img_cats_sc_txt']
    color_name = data['color_name']
    color_512 = data['color_512']
    color_1 = data['color_1']
    color_1_hex = data['color_1_hex']
    color_2 = data['color_2']
    color_2_hex = data['color_2_hex']
    color_3 = data['color_3']
    color_3_hex = data['color_3_hex']
    encoding_nocrop = data['encoding_nocrop']
    encoding_crop = data['encoding_crop']
    encoding_squarecrop = data['encoding_squarecrop']

    product_submission = Images(
        img_hash=img_hash,
        prod_url=prod_url,
        img_url=img_url,
        name=name,
        description=description,
        brand=brand,
        shop=shop,
        date=date,
        sex=sex,
        currency=currency,
        price=price,
        sale=sale,
        saleprice=saleprice,
        spider_cat=spider_cat,
        img_cats_ai_txt=img_cats_ai_txt,
        img_cats_sc_txt=img_cats_sc_txt,
        color_name=color_name,
        color_512=color_512,
        color_1=color_1,
        color_1_hex=color_1_hex,
        color_2=color_2,
        color_2_hex=color_2_hex,
        color_3=color_3,
        color_3_hex=color_3_hex,
        encoding_nocrop=encoding_nocrop,
        encoding_crop=encoding_crop,
        encoding_squarecrop=encoding_squarecrop
    )

    try:
        existing_image = Images.query.filter_by(img_hash=img_hash).first()
    except:
        existing_image = None

    if existing_image is None:
        print('Adding a new product')
        db.session.add(product_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('Updating existing product')

        existing_image.prod_url = prod_url
        existing_image.name = name
        existing_image.description = description
        existing_image.brand = brand
        existing_image.shop = shop
        existing_image.date = date
        existing_image.sex = sex
        existing_image.currency = currency
        existing_image.price = price
        existing_image.sale = sale
        existing_image.saleprice = saleprice
        existing_image.img_url = img_url
        existing_image.spider_cat = spider_cat
        existing_image.img_cats_ai_txt = img_cats_ai_txt
        existing_image.img_cats_sc_txt = img_cats_sc_txt
        existing_image.color_name = color_name
        existing_image.color_512 = color_512
        existing_image.color_1 = color_1
        existing_image.color_1_hex = color_1_hex
        existing_image.color_2 = color_2
        existing_image.color_2_hex = color_2_hex
        existing_image.color_3 = color_3
        existing_image.color_3_hex = color_3_hex
        existing_image.encoding_nocrop = encoding_nocrop
        existing_image.encoding_crop = encoding_crop
        existing_image.encoding_squarecrop = encoding_squarecrop

        db.session.commit()

        return json.dumps(True)


def image_commit_v2(db, ImagesV2, data):
    img_hash = data['img_hash']
    img_url = data['img_url']
    prod_id = data['prod_id']
    prod_url = data['prod_url']
    color_string = data['color_string']
    date = data['date']
    name = data['name']
    price = data['price']
    sale = data['sale']
    saleprice = data['saleprice']
    sex = data['sex']
    shop = data['shop']
    kind_cats = data['kind_cats']
    color_pattern_cats = data['color_pattern_cats']
    style_cats = data['style_cats']
    material_cats = data['material_cats']
    attribute_cats = data['attribute_cats']
    filter_cats = data['filter_cats']
    all_cats = data['all_cats']
    kind_arr = data['kind_arr']
    col_pat_arr = data['col_pat_arr']
    style_arr = data['style_arr']
    material_arr = data['material_arr']
    attr_arr = data['attr_arr']
    filter_arr = data['filter_arr']
    all_arr = data['all_arr']
    color_1 = data['color_1']
    color_1_hex = data['color_1_hex']
    color_2 = data['color_2']
    color_2_hex = data['color_2_hex']
    color_3 = data['color_3']
    color_3_hex = data['color_3_hex']
    encoding_crop = data['encoding_crop']
    size_stock = data['size_stock']
    in_stock = data['in_stock']

    product_submission = ImagesV2(
        img_hash=img_hash,
        img_url=img_url,
        prod_id=prod_id,
        prod_url=prod_url,
        color_string=color_string,
        date=date,
        name=name,
        price=price,
        sale=sale,
        saleprice=saleprice,
        sex=sex,
        shop=shop,
        kind_cats=kind_cats,
        color_pattern_cats=color_pattern_cats,
        style_cats=style_cats,
        material_cats=material_cats,
        attribute_cats=attribute_cats,
        filter_cats=filter_cats,
        all_cats=all_cats,
        kind_arr=kind_arr,
        col_pat_arr=col_pat_arr,
        style_arr=style_arr,
        material_arr=material_arr,
        attr_arr=attr_arr,
        filter_arr=filter_arr,
        all_arr=all_arr,
        color_1=color_1,
        color_1_hex=color_1_hex,
        color_2=color_2,
        color_2_hex=color_2_hex,
        color_3=color_3,
        color_3_hex=color_3_hex,
        encoding_crop=encoding_crop,
        size_stock=size_stock,
        in_stock=in_stock
    )

    try:
        existing_image = ImagesV2.query.filter_by(img_hash=img_hash).first()
    except:
        existing_image = None

    if existing_image is None:
        print('Adding a new product')
        db.session.add(product_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('Updating existing product')

        existing_image.img_url = img_url
        existing_image.prod_id = prod_id
        existing_image.prod_url = prod_url
        existing_image.color_string = color_string
        existing_image.date = date
        existing_image.name = name
        existing_image.price = price
        existing_image.sale = sale
        existing_image.price = price
        existing_image.sale = sale
        existing_image.saleprice = saleprice
        existing_image.sex = sex
        existing_image.shop = shop
        existing_image.kind_cats = kind_cats
        existing_image.color_pattern_cats = color_pattern_cats
        existing_image.style_cats = style_cats
        existing_image.material_cats = material_cats
        existing_image.attribute_cats = attribute_cats
        existing_image.filter_cats = filter_cats
        existing_image.all_cats = all_cats
        existing_image.kind_arr = kind_arr
        existing_image.col_pat_arr = col_pat_arr
        existing_image.style_arr = style_arr
        existing_image.material_arr = material_arr
        existing_image.attr_arr = attr_arr
        existing_image.filter_arr = filter_arr
        existing_image.all_arr = all_arr
        existing_image.color_1 = color_1
        existing_image.color_1_hex = color_1_hex
        existing_image.color_2 = color_2
        existing_image.color_2_hex = color_2_hex
        existing_image.color_3 = color_3
        existing_image.color_3_hex = color_3_hex
        existing_image.encoding_crop = encoding_crop
        existing_image.size_stock = size_stock
        existing_image.in_stock = in_stock

        db.session.commit()

        return json.dumps(True)


def image_commit_v2_skinny(db, ImagesV2Skinny, data):
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
    color_pattern_cats = data['color_pattern_cats']
    style_cats = data['style_cats']
    material_cats = data['material_cats']
    attribute_cats = data['attribute_cats']
    filter_cats = data['filter_cats']
    all_cats = data['all_cats']
    size_stock = data['size_stock']
    in_stock = data['in_stock']

    img_data_submission = ImagesV2Skinny(
        img_hash=img_hash,
        img_url=img_url,
        prod_id=prod_id,
        prod_url=prod_url,
        brand=brand,
        color_string=color_string,
        date=date,
        name=name,
        price=price,
        sale=sale,
        saleprice=saleprice,
        discount_rate=discount_rate,
        sex=sex,
        shop=shop,
        kind_cats=kind_cats,
        color_pattern_cats=color_pattern_cats,
        style_cats=style_cats,
        material_cats=material_cats,
        attribute_cats=attribute_cats,
        filter_cats=filter_cats,
        all_cats=all_cats,
        size_stock=size_stock,
        in_stock=in_stock
    )

    try:
        existing_image = ImagesV2Skinny.query.filter_by(img_hash=img_hash).first()
    except:
        existing_image = None

    if existing_image is None:
        print('Adding a new product')
        db.session.add(img_data_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('Updating existing product')

        existing_image.img_url = img_url
        existing_image.prod_id = prod_id
        existing_image.prod_url = prod_url
        existing_image.brand = brand
        existing_image.color_string = color_string
        existing_image.date = date
        existing_image.name = name
        existing_image.price = price
        existing_image.sale = sale
        existing_image.saleprice = saleprice
        existing_image.discount_rate = discount_rate
        existing_image.sex = sex
        existing_image.shop = shop
        existing_image.kind_cats = kind_cats
        existing_image.color_pattern_cats = color_pattern_cats
        existing_image.style_cats = style_cats
        existing_image.material_cats = material_cats
        existing_image.attribute_cats = attribute_cats
        existing_image.filter_cats = filter_cats
        existing_image.all_cats = all_cats
        existing_image.size_stock = size_stock
        existing_image.in_stock = in_stock

        db.session.commit()

        return json.dumps(True)


def product_commit(db, Products, data):
    prod_hash = data['prod_hash']
    prod_url = data['prod_url']
    name = data['name']
    description = data['description']
    brand = data['brand']
    shop = data['shop']
    date = data['date']
    sex = data['sex']
    currency = data['currency']
    price = data['price']
    sale = data['sale']
    saleprice = data['saleprice']
    img_url = data['img_url']
    img_urls = data['img_urls']
    img_hashes = data['img_hashes']
    spider_cat = data['spider_cat']
    img_cats_sc_txt = data['img_cats_sc_txt']

    product_submission = Products(
        prod_hash=prod_hash,
        prod_url=prod_url,
        name=name,
        description=description,
        brand=brand,
        shop=shop,
        date=date,
        sex=sex,
        currency=currency,
        price=price,
        sale=sale,
        saleprice=saleprice,
        img_url=img_url,
        img_urls=img_urls,
        img_hashes=img_hashes,
        spider_cat=spider_cat,
        img_cats_sc_txt=img_cats_sc_txt
    )

    try:
        existing_product = Products.query.filter_by(prod_hash=prod_hash).first()
    except:
        existing_product = None

    if existing_product is None:
        print('Adding a new product')
        db.session.add(product_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('Updating existing product')

        existing_product.prod_hash = prod_hash
        existing_product.prod_url = prod_url
        existing_product.name = name
        existing_product.description = description
        existing_product.brand = brand
        existing_product.shop = shop
        existing_product.date = date
        existing_product.sex = sex
        existing_product.currency = currency
        existing_product.price = price
        existing_product.sale = sale
        existing_product.saleprice = saleprice
        existing_product.img_url = img_url
        existing_product.img_urls = img_urls
        existing_product.img_hashes = img_hashes
        existing_product.spider_cat = spider_cat
        existing_product.img_cats_sc_txt = img_cats_sc_txt

        db.session.commit()

        return json.dumps(True)


def product_commit_v2(db, ProductsV2, data):
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
    sex = data['sex']
    shop = data['shop']
    size_stock = data['size_stock']
    kind_cats = data['kind_cats']
    color_pattern_cats = data['color_pattern_cats']
    style_cats = data['style_cats']
    material_cats = data['material_cats']
    attribute_cats = data['attribute_cats']
    filter_cats = data['filter_cats']
    all_cats = data['all_cats']
    kind_arr = data['kind_arr']
    col_pat_arr = data['col_pat_arr']
    style_arr = data['style_arr']
    material_arr = data['material_arr']
    attr_arr = data['attr_arr']
    filter_arr = data['filter_arr']
    all_arr = data['all_arr']

    product_submission = ProductsV2(
        prod_id=prod_id,
        name=name,
        prod_url=prod_url,
        brand=brand,
        category=category,
        color_string=color_string,
        currency=currency,
        date=date,
        description=description,
        image_hash=image_hash,
        image_urls=image_urls,
        price=price,
        sale=sale,
        saleprice=saleprice,
        sex=sex,
        shop=shop,
        size_stock=size_stock,
        kind_cats=kind_cats,
        color_pattern_cats=color_pattern_cats,
        style_cats=style_cats,
        material_cats=material_cats,
        attribute_cats=attribute_cats,
        filter_cats=filter_cats,
        all_cats=all_cats,
        kind_arr=kind_arr,
        col_pat_arr=col_pat_arr,
        style_arr=style_arr,
        material_arr=material_arr,
        attr_arr=attr_arr,
        filter_arr=filter_arr,
        all_arr=all_arr
    )

    try:
        existing_product = ProductsV2.query.filter_by(prod_id=prod_id).first()
    except:
        existing_product = None

    if existing_product is None:
        print('Adding a new product')
        db.session.add(product_submission)
        db.session.commit()
        return json.dumps(True)

    else:
        print('Updating existing product')

        existing_product.name = name
        existing_product.prod_url = prod_url
        existing_product.brand = brand
        existing_product.category = category
        existing_product.color_string = color_string
        existing_product.currency = currency
        existing_product.date = date
        existing_product.description = description
        existing_product.image_hash = image_hash
        existing_product.image_urls = image_urls
        existing_product.price = price
        existing_product.sale = sale
        existing_product.saleprice = saleprice
        existing_product.sex = sex
        existing_product.shop = shop
        existing_product.size_stock = size_stock
        existing_product.kind_cats = kind_cats
        existing_product.color_pattern_cats = color_pattern_cats
        existing_product.style_cats = style_cats
        existing_product.material_cats = material_cats
        existing_product.attribute_cats = attribute_cats
        existing_product.filter_cats = filter_cats
        existing_product.all_cats = all_cats
        existing_product.kind_arr = kind_arr
        existing_product.col_pat_arr = col_pat_arr
        existing_product.style_arr = style_arr
        existing_product.material_arr = material_arr
        existing_product.attr_arr = attr_arr
        existing_product.filter_arr = filter_arr
        existing_product.all_arr = all_arr

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
