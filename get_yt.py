import urllib.request
import re

urls = [
    'https://www.youtube.com/shorts/ko3uUYdafos',
    'https://www.youtube.com/shorts/5xpM-hsYo3w'
]

for url in urls:
    print('Fetching:', url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            title = re.search(r'<title>(.*?)</title>', html)
            print('Title:', title.group(1) if title else 'No title')
            og_title = re.search(r'property="og:title" content="(.*?)"', html)
            print('OG Title:', og_title.group(1) if og_title else 'No og_title')
            og_desc = re.search(r'property="og:description" content="(.*?)"', html)
            print('OG Desc:', og_desc.group(1) if og_desc else 'No og_desc')
            tags = re.findall(r'"tag":"(.*?)"', html)
            print('Tags:', tags[:10])
    except Exception as e:
        print('Error:', e)
    print('-'*40)
