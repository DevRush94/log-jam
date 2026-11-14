from PIL import Image
import numpy as np

p1 = r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\ko3uUYdafos.jpg'
im = Image.open(p1)
w, h = im.size

# The center 9:16 vertical mobile frame
# For height 720, width 9/16 * 720 = 405!
# Center x is 640, so 640 - 202 = 438 to 640 + 202 = 842!
# Exactly [438, 842]! That matches our bounding box [438, 829] exactly!
crop_mobile = im.crop((438, 0, 842, 720))
crop_mobile.save("mobile_frame_ko3u.png")
print("Saved mobile_frame_ko3u.png, size:", crop_mobile.size)

# Analyze mobile frame colors and structure
arr = np.array(crop_mobile)
print("Mobile frame mean RGB:", arr.mean(axis=(0,1)).astype(int))

# Analyze top 20% (HUD) of mobile frame
hud = arr[:int(720 * 0.15), :, :]
print("HUD mean RGB:", hud.mean(axis=(0,1)).astype(int))

# Check for bright colors inside the mobile frame
def check_mobile_colors(name, min_rgb, max_rgb):
    mask = (
        (arr[:,:,0] >= min_rgb[0]) & (arr[:,:,0] <= max_rgb[0]) &
        (arr[:,:,1] >= min_rgb[1]) & (arr[:,:,1] <= max_rgb[1]) &
        (arr[:,:,2] >= min_rgb[2]) & (arr[:,:,2] <= max_rgb[2])
    )
    y_idx, x_idx = np.where(mask)
    if len(x_idx) > 0:
        print(f"Mobile [{name}]: {len(x_idx)} px, center at x={int(x_idx.mean())}, y={int(y_idx.mean())}, bbox: x:[{x_idx.min()},{x_idx.max()}], y:[{y_idx.min()},{y_idx.max()}]")

check_mobile_colors("Bright Orange", (180, 60, 0), (255, 140, 40))
check_mobile_colors("Bright Green Grass", (80, 160, 40), (160, 240, 100))
check_mobile_colors("Dark Forest Conifers", (10, 40, 10), (50, 90, 40))
check_mobile_colors("Road Grey", (40, 40, 40), (80, 80, 80))
check_mobile_colors("Wood / Lumber Brown", (130, 80, 30), (220, 160, 80))
check_mobile_colors("White Elements", (220, 220, 220), (255, 255, 255))
