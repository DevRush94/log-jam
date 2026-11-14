from PIL import Image
import numpy as np

im = Image.open('test_screen.png')
w, h = im.size
print(f"Current game screenshot: {w}x{h}")

arr = np.array(im)
# Check dominant color
# Find where the machines/conveyor/trucks are in the screenshot
# The grass in our game is 0x4ade80 (RGB ~ 74, 222, 128)
# Saws are at -8 to 2
# Let's inspect where pixels differ from background
bg_color = np.array([219, 234, 254]) # 0xdbeafe
diff = np.abs(arr[:,:,:3] - bg_color).sum(axis=2)
content_pixels = np.where(diff > 30)
if len(content_pixels[0]) > 0:
    min_y, max_y = content_pixels[0].min(), content_pixels[0].max()
    min_x, max_x = content_pixels[1].min(), content_pixels[1].max()
    print(f"Rendered content area: x:[{min_x}, {max_x}] ({max_x - min_x}px), y:[{min_y}, {max_y}] ({max_y - min_y}px)")
    print(f"Content occupies {(len(content_pixels[0]) / (w*h)) * 100:.1f}% of screen")
