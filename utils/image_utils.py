import cv2
from PIL import Image

def read_image(path):
    img = Image.open(path)
    return img


def save_image(path,img):
    cv2.imwrite(path,img)