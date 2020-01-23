import asyncio
import aiohttp
import json
import endpoints


async def send_file(url, image_file):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            'image': image_file
        }) as response:
            data = await response.text()
            # print(data)
            return data


def get_features(image):
    cat_api = endpoints.CAT_API_PATH
    color_enc_api = endpoints.COLOR_ENC_API_PATH
    vgg16_enc_api = endpoints.VGG16_API_PATH

    api_urls = [
        color_enc_api,
        cat_api,
        vgg16_enc_api
    ]

    tasks = [send_file(url, image) for url in api_urls]
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    color_encoding_res, cat_res, vgg16_enc_res = loop.run_until_complete(asyncio.gather(*tasks))

    img_cats_ai_txt = json.loads(cat_res)['res']['img_cats_ai_txt']
    crop_enc = json.loads(color_encoding_res)['encoding']
    vgg16_enc = json.loads(vgg16_enc_res)

    color_res = json.loads(color_encoding_res)['color']
    color_1 = color_res['color_1']
    color_1_hex = color_res['color_1_hex']
    color_2 = color_res['color_2']
    color_2_hex = color_res['color_2_hex']
    color_3 = color_res['color_3']
    color_3_hex = color_res['color_3_hex']

    results = {
        'img_cats_ai_txt': img_cats_ai_txt,
        'colors': {
            'color_1': color_1,
            'color_1_hex': color_1_hex,
            'color_2': color_2,
            'color_2_hex': color_2_hex,
            'color_3': color_3,
            'color_3_hex': color_3_hex
        },
        'rcnn_encoding': crop_enc,
        'vgg16_encoding': vgg16_enc
    }
    return results
