from PIL import Image
import numpy as np

p1 = r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\ko3uUYdafos.jpg'
im = Image.open(p1)
w, h = im.size
print(f"Loaded {p1}: {w}x{h}")

# Let's save a series of crops for analysis:
# 1. Top HUD (0% to 20% height)
# 2. Upper Middle (20% to 40%)
# 3. Center (40% to 60%)
# 4. Lower Middle (60% to 80%)
# 5. Bottom HUD (80% to 100%)
# 6. Left side, Right side
crops = {
    'hud_top': (0, 0, w, int(h * 0.18)),
    'upper_mid': (0, int(h * 0.18), w, int(h * 0.45)),
    'center': (0, int(h * 0.45), w, int(h * 0.75)),
    'bottom': (0, int(h * 0.75), w, h),
    'center_detail': (int(w * 0.25), int(h * 0.25), int(w * 0.75), int(h * 0.75))
}

for name, box in crops.items():
    cropped = im.crop(box)
    cropped.save(f"crop_{name}.png")
    arr = np.array(cropped)
    # Find most common colors
    print(f"Crop {name}: size {cropped.size}, mean RGB: {arr.mean(axis=(0,1)).astype(int)}")
