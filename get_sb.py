import urllib.request
import re

for vid in ['ko3uUYdafos', '5xpM-hsYo3w']:
    url = f'https://www.youtube.com/watch?v={vid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            sb = re.findall(r'https://[^\"]*?storyboard[^\"]*', html)
            print(f'{vid} storyboards:', sb)
    except Exception as e:
        print(vid, 'error:', e)
