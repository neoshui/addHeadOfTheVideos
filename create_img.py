from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np


def draw_img(new_img, text):
    text = str(text)
    draw = ImageDraw.Draw(new_img)
    img_size = new_img.size
    draw.line((0, 0) + img_size, fill=128)
    draw.line((0, img_size[1], img_size[0], 0), fill=128)
    font_size = 40
    font = ImageFont.truetype('STHeitiMedium.ttc', font_size)
    img_font_size = font.getsize(text)
    while img_font_size[0] > img_size[0]:
        font_size -= 5
        font = ImageFont.truetype('STHeitiMedium.ttc', font_size)
        img_font_size = font.getsize(text)
    x = (img_size[0] - img_font_size[0]) / 2
    y = (img_size[1] - img_font_size[1]) / 2
    draw.text((x, y), text, font=font, fill=(25, 25, 25))
    pass


def create_img(width, height, text='default', color=(100, 100, 100, 100)):
    new_img = Image.new('RGBA', (int(width), int(height)), color)
    draw_img(new_img, text)
    new_img.save('f.png')
    pass


if __name__ == '__main__':
    create_img(100, 200,text='这是测试')
