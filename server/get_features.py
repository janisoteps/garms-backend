import asyncio
import aiohttp
import json


async def send_file(url, image_file):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            'image': image_file
        }) as response:
            data = await response.text()
            print(data)
            return data


def get_features(image):
    # color_512_api = 'http://34.245.151.12/api/color512'
    nocrop_encoding_api = 'http://34.248.180.130/api/encoding'
    cat_api = 'http://34.245.0.175/api/cats'
    color_api = 'https://hvoe2gb7cf.execute-api.eu-west-1.amazonaws.com/production/api/color'
    # crop_encoding_api = 'http://34.251.45.220/api/encoding'
    # sqcrop_encoding_api = 'http://34.244.2.76/api/encoding'

    api_urls = [
        nocrop_encoding_api,
        color_api,
        cat_api,
        # color_512_api,
        # crop_encoding_api,
        # sqcrop_encoding_api
    ]

    tasks = [send_file(url, image) for url in api_urls]

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    # Gather responses from APIs using asyncio
    # print(len(loop.run_until_complete(asyncio.gather(*tasks))))
    nocrop_enc_res, color_res, cat_res = loop.run_until_complete(asyncio.gather(*tasks))

    img_cats_ai_txt = json.loads(cat_res)['res']['img_cats_ai_txt']
    alt_cats_txt = json.loads(cat_res)['res']['alt_cats_txt']

    print('Img cats: ', str(img_cats_ai_txt))

    # color_512 = json.loads(color_512_res)['res']['color_512']
    nocrop_enc = json.loads(nocrop_enc_res)['res']['encoding_nocrop']
    # crop_enc = json.loads(crop_enc_res)['res']['encoding_crop']
    # sqcrop_enc = json.loads(sqcrop_enc_res)['res']['encoding_sqcrop']

    for img_cat_ai in img_cats_ai_txt:
        if img_cat_ai in alt_cats_txt:
            alt_cats_txt.remove(img_cat_ai)

    color_1 = json.loads(color_res)['res']['color_1']
    color_1_hex = json.loads(color_res)['res']['color_1_hex']
    color_2 = json.loads(color_res)['res']['color_2']
    color_2_hex = json.loads(color_res)['res']['color_2_hex']
    color_3 = json.loads(color_res)['res']['color_3']
    color_3_hex = json.loads(color_res)['res']['color_3_hex']

    results = {
        'img_cats_ai_txt': img_cats_ai_txt,
        'alt_cats_txt': alt_cats_txt,
        'colors': {
            'color_1': color_1,
            'color_1_hex': color_1_hex,
            'color_2': color_2,
            'color_2_hex': color_2_hex,
            'color_3': color_3,
            'color_3_hex': color_3_hex
        },
        # 'color_512': color_512,
        'encoding_nocrop': nocrop_enc,
        # 'encoding_crop': crop_enc,
        # 'encoding_squarecrop': sqcrop_enc
    }

    return results
