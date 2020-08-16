import os

from PIL import Image, ImageDraw, ImageFont
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np


class Videos:
    def __init__(self):
        pass

    def draw_img(self, new_img, text, logo_text):
        text = str(text)
        logo_text = str(logo_text)
        draw = ImageDraw.Draw(new_img)
        img_size = new_img.size
        # draw.line((0, 0) + img_size, fill=128)
        # draw.line((0, img_size[1], img_size[0], 0), fill=128)

        title_font_size = 100
        title_font = ImageFont.truetype('STHeitiMedium.ttc', title_font_size)
        title_img_font_size = title_font.getsize(text)
        while title_img_font_size[0] > img_size[0]:
            title_font_size -= 5
            title_font = ImageFont.truetype('STHeitiMedium.ttc', title_font_size)
            title_img_font_size = title_font.getsize(text)

        logo_font_size = 90
        logo_font = ImageFont.truetype('STHeitiMedium.ttc', logo_font_size)
        logo_img_font_size = logo_font.getsize(text)

        title_x = (img_size[0] - title_img_font_size[0]) / 2
        title_y = (img_size[1] - title_img_font_size[1]) / 2
        logo_x = (img_size[0] - (logo_img_font_size[0]))
        logo_y = (img_size[1] - (logo_img_font_size[1]))
        print(img_size[0], img_size[1])
        print(logo_img_font_size[0], logo_img_font_size[1])
        print(logo_x, logo_y)

        draw.text((title_x, title_y), text, font=title_font, fill=(25, 25, 25))
        draw.text((logo_x, logo_y), logo_text, font=title_font, fill=(25, 25, 25))
        pass

    def create_img(self, width, height, text='title', logo_text='logo', color=(100, 100, 100, 100)):
        new_img = Image.new('RGBA', (int(width), int(height)), color)
        self.draw_img(new_img, text, logo_text)
        new_img.save(f'{text}.png')
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
            return [fps, width, height, file_name]
        else:
            return []

    def gen_file(self, path):
        files_list = os.listdir(path)
        file_list = []
        for file in files_list:
            if not os.path.isdir(file):
                file_list.append(file)
        return file_list


if __name__ == '__main__':
    v = Videos()
    # v.create_img(100, 200, text='这是测试')
    files = v.gen_file('./')
    for file in files:
        video_info = v.get_video_info(file)
        if video_info != []:
            v.create_img(video_info[1], video_info[2], video_info[3], 'logo')
