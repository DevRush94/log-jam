from PIL import Image
import numpy as np

p2 = r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\5xpM-hsYo3w.jpg'
im2 = Image.open(p2)
crop_mobile2 = im2.crop((438, 0, 842, 720))
crop_mobile2.save("mobile_frame_5xp.png")
print("Saved mobile_frame_5xp.png, size:", crop_mobile2.size)

arr2 = np.array(crop_mobile2)
print("Mobile frame 2 mean RGB:", arr2.mean(axis=(0,1)).astype(int))

def check_mobile_colors2(name, min_rgb, max_rgb):
    mask = (
        (arr2[:,:,0] >= min_rgb[0]) & (arr2[:,:,0] <= max_rgb[0]) &
        (arr2[:,:,1] >= min_rgb[1]) & (arr2[:,:,1] <= max_rgb[1]) &
        (arr2[:,:,2] >= min_rgb[2]) & (arr2[:,:,2] <= max_rgb[2])
    )
    y_idx, x_idx = np.where(mask)
    if len(x_idx) > 0:
        print(f"Mobile 2 [{name}]: {len(x_idx)} px, center at x={int(x_idx.mean())}, y={int(y_idx.mean())}, bbox: x:[{x_idx.min()},{x_idx.max()}], y:[{y_idx.min()},{y_idx.max()}]")

check_mobile_colors2("Bright Orange (Trucks)", (180, 60, 0), (255, 140, 40))
check_mobile_colors2("Bright Red (Emoji)", (180, 20, 20), (255, 70, 70))
check_mobile_colors2("Bright Yellow/Gold", (200, 160, 20), (255, 240, 80))
check_mobile_colors2("Bright Green (Upgrade Pad)", (20, 160, 60), (90, 230, 140))
check_mobile_colors2("Wood / Lumber Brown", (130, 80, 30), (220, 160, 80))
check_mobile_colors2("White Elements", (220, 220, 220), (255, 255, 255))
