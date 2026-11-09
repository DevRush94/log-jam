import urllib.request

for vid in ['ko3uUYdafos', '5xpM-hsYo3w']:
    url = f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg'
    try:
        urllib.request.urlretrieve(url, f'{vid}.jpg')
        print(f'Downloaded {vid}.jpg')
    except Exception as e:
        url2 = f'https://img.youtube.com/vi/{vid}/hqdefault.jpg'
        urllib.request.urlretrieve(url2, f'{vid}.jpg')
        print(f'Downloaded fallback {vid}.jpg')
