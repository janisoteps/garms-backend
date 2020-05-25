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


def get_features_light(image):
    cat_api = endpoints.CAT_API_PATH
    vgg16_enc_api = endpoints.VGG16_API_PATH

    api_urls = [
        cat_api,
        vgg16_enc_api
    ]
    tasks = [send_file(url, image) for url in api_urls]
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    cat_res, vgg16_enc_res = loop.run_until_complete(asyncio.gather(*tasks))

    img_cats_ai_txt = json.loads(cat_res)['res']['img_cats_ai_txt']
    vgg16_enc = json.loads(vgg16_enc_res)

    results = {
        'img_cats_ai_txt': img_cats_ai_txt,
        'vgg16_encoding': vgg16_enc
    }
    return results
