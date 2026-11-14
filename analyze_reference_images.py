from PIL import Image
import numpy as np

for name in ['ko3uUYdafos.jpg', '5xpM-hsYo3w.jpg']:
    p = r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\\' + name
    im = Image.open(p)
    w, h = im.size
    print(f"=== {name} ({w}x{h}) ===")
    
    # Analyze sections: top, middle, bottom
    top = np.array(im.crop((0, 0, w, int(h * 0.25))))
    mid = np.array(im.crop((0, int(h * 0.25), w, int(h * 0.75))))
    bot = np.array(im.crop((0, int(h * 0.75), w, h)))
    
    print("Top mean color RGB:", top.mean(axis=(0,1)).astype(int))
    print("Mid mean color RGB:", mid.mean(axis=(0,1)).astype(int))
    print("Bot mean color RGB:", bot.mean(axis=(0,1)).astype(int))
