import os

from PIL import Image, ImageDraw, ImageFont
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np


class Videos:
    def __init__(self):
        pass

    def draw_img(self, new_img, text):
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

    def create_img(self, width, height, text='default', color=(100, 100, 100, 100)):
        new_img = Image.new('RGBA', (int(width), int(height)), color)
        self.draw_img(new_img, text)
        new_img.save('f.png')
        pass

    def get_video_info(self, file):
        file_type = file.split('.')[-1]
        if file_type == 'mp4' or file_type == 'MP4' or file_type == 'avi' or file_type == 'AVI':
            cap = cv2.VideoCapture(file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            file_name = file.split('.')[0]

            print(fps, width, height, file_name)

    def gen_file(self, path):
        files_list = os.listdir(path)
        file_list = []
        for file in files_list:
            if not os.path.isdir(path + '/' + file):
                file_list.append(file)
                self.get_video_info(file)


if __name__ == '__main__':
    v = Videos()
    # v.create_img(100, 200, text='这是测试')
    v.gen_file('./')
