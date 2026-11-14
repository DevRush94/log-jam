from PIL import Image
import numpy as np

p1 = r'C:\Users\DELL\.gemini\antigravity\brain\54d18a4a-1ef2-4368-8be2-f77913715cd9\ko3uUYdafos.jpg'
im = Image.open(p1)
w, h = im.size

# Let's inspect small patches to see where UI elements and game objects are located
# Let's check for bright yellow / gold, bright red, orange, white, and cyan pixels
arr = np.array(im)

def find_color_regions(name, min_rgb, max_rgb):
    mask = (
        (arr[:,:,0] >= min_rgb[0]) & (arr[:,:,0] <= max_rgb[0]) &
        (arr[:,:,1] >= min_rgb[1]) & (arr[:,:,1] <= max_rgb[1]) &
        (arr[:,:,2] >= min_rgb[2]) & (arr[:,:,2] <= max_rgb[2])
    )
    y_indices, x_indices = np.where(mask)
    if len(x_indices) > 0:
        print(f"[{name}] {len(x_indices)} pixels. Bounding box: x:[{x_indices.min()}, {x_indices.max()}], y:[{y_indices.min()}, {y_indices.max()}]")
    else:
        print(f"[{name}] 0 pixels found.")

print(f"Image dimensions: {w}x{h}")
# Bright Orange (Trucks)
find_color_regions("Orange (Trucks)", (200, 70, 0), (255, 160, 50))
# Bright Red (Angry emoji / signs / buttons)
find_color_regions("Red (Emoji/Icons)", (200, 0, 0), (255, 60, 60))
# Bright Yellow/Gold (Coins / Stars / Badges)
find_color_regions("Yellow/Gold (Money/Stars)", (220, 180, 0), (255, 255, 60))
# White (Text / Dashed road lines / Icons)
find_color_regions("White (Text/Dashes)", (240, 240, 240), (255, 255, 255))
# Bright Cyan / Blue (River / Sky / UI)
find_color_regions("Cyan/Blue (Water/UI)", (0, 150, 200), (80, 230, 255))
# Wood Planks / Timber (Warm Brown / Tan)
find_color_regions("Wood Planks (Tan/Amber)", (160, 100, 40), (230, 170, 90))
