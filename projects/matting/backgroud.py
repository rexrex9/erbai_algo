from PIL import Image
from data import filepath as fp




class BackGround():

    def __init__(self):
        pass

    def put_together(self,img,bg):
        if bg:
            bg = Image.open(bg)
        else:
            bg = Image.open(fp.FILE_TEST.DEFAULT_GREEN_PNG)
        img = Image.open(img)

        background_img = bg.resize(img.size)
        new_img = Image.new('RGBA', img.size)
        new_img.paste(background_img, (0, 0))

        new_img.paste(img, (0, 0), mask=img)
        return new_img


