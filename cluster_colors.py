from PIL import Image
import numpy as np

def analyze_palette(image_path, name):
    im = Image.open(image_path).convert('RGB')
    # Resize for fast clustering
    small = im.resize((160, 90))
    pixels = np.array(small).reshape(-1, 3)
    
    # Quantize colors into buckets of 32
    buckets = {}
    for r, g, b in pixels:
        key = ((r // 24) * 24, (g // 24) * 24, (b // 24) * 24)
        buckets[key] = buckets.get(key, 0) + 1
    
    sorted_buckets = sorted(buckets.items(), key=lambda x: x[1], reverse=True)
    print(f"\n=== Dominant Colors for {name} ===")
    total = len(pixels)
    for color, count in sorted_buckets[:12]:
        hex_code = '#{:02x}{:02x}{:02x}'.format(*color)
        pct = (count / total) * 100
        print(f"  RGB: {color} | Hex: {hex_code} | {pct:.1f}%")

analyze_palette(r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\ko3uUYdafos.jpg', 'ko3uUYdafos.jpg')
analyze_palette(r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\5xpM-hsYo3w.jpg', '5xpM-hsYo3w.jpg')
