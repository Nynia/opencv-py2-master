import cv2


from PIL import Image

img = Image.open("img/20200603230612.png")
cropped = img.crop((172, 529, 366, 594))
cropped.save('ok2.')