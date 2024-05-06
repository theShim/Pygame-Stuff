#put images that need transparency in 'transparent_images' folder
import os
from PIL import Image

key = (255, 255, 255)

for filename in os.listdir("transparent_images/"):
    name, ext = os.path.splitext(filename)

    img = Image.open(f"transparent_images/{filename}")
    img = img.convert("RGBA")
    data = img.getdata()

    newData = []
    for item in data:
        if item[0] == key[0] and item[1] == key[1] and item[2] == key[2]:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(f"transparent_output/{name}_transparent.png", "PNG")
print("done")