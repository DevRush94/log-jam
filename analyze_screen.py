from PIL import Image

im = Image.open("test_screen.png")
print("Image size:", im.size)
colors = im.getcolors(maxcolors=100000)
print("Unique colors:", len(colors) if colors else "many")
if colors:
    # Sort by count
    colors.sort(reverse=True, key=lambda x: x[0])
    for count, col in colors[:10]:
        print(f"Count: {count}, Color: {col}")
