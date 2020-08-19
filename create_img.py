import os

from PIL import Image, ImageDraw, ImageFont
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np


class Videos:
    def __init__(self):
        pass

    def draw_img(self, new_img, title_text, logo_text):
        """
        将文字放到图片上
        :param new_img:背景图片
        :param title_text:文件标题
        :param logo_text:logo标题
        :return:
        """
        title_text = str(title_text)
        logo_text = str(logo_text)
        draw = ImageDraw.Draw(new_img)
        img_size = new_img.size
        # draw.line((0, 0) + img_size, fill=128)
        # draw.line((0, img_size[1], img_size[0], 0), fill=128)

        title_font_size = 100
        title_font = ImageFont.truetype('STHeitiMedium.ttc', title_font_size)
        title_img_font_size = title_font.getsize(title_text)
        while title_img_font_size[0] > img_size[0]:
            title_font_size -= 5
            title_font = ImageFont.truetype('STHeitiMedium.ttc', title_font_size)
            title_img_font_size = title_font.getsize(title_text)

        logo_font_size = 100
        logo_font = ImageFont.truetype('STHeitiMedium.ttc', logo_font_size)
        logo_img_font_size = logo_font.getsize(logo_text)

        title_x = (img_size[0] - title_img_font_size[0]) / 2
        title_y = (img_size[1] - title_img_font_size[1]) / 2
        logo_x = (img_size[0] - (logo_img_font_size[0] + 30))
        logo_y = (img_size[1] - (logo_img_font_size[1] + 30))
        # print('img', img_size[0], img_size[1])
        # print('logo', logo_img_font_size[0], logo_img_font_size[1])
        # print('xy', logo_x, logo_y)

        draw.text((title_x, title_y), title_text, font=title_font, fill=(25, 25, 25))
        draw.text((logo_x, logo_y), logo_text, font=title_font, fill=(25, 25, 25))

        pass

    def add_img_logo(self, new_img, icon):
        """
        粘贴logo图标
        :param new_img: 背景图片
        :param icon: logo
        :return:
        """
        # img_size = new_img.size
        logo_img = Image.open(icon)
        new_img.paste(logo_img, (40, 40))
        return new_img

        pass

    def create_img(self, width, height, text='title', logo_text='logo', color=(100, 100, 100, 100)):
        """
        创建背景图片
        :param width:视频宽度
        :param height:视频高度
        :param text:视频标题
        :param logo_text:logo文字
        :param color:
        :return:
        """
        new_img = Image.new('RGBA', (int(width), int(height)), color)
        self.draw_img(new_img, text, logo_text)
        new_img = self.add_img_logo(new_img, 'icon.png')
        new_img.save(f'{text}.png')
        pass

    def get_video_info(self, file):
        """
        获取视频信息：fps,width,height,file_name
        :param file:视频文件
        :return:
        """
        file_type = file.split('.')[-1]
        if file_type == 'mp4' or file_type == 'MP4' or file_type == 'avi' or file_type == 'AVI':
            cap = cv2.VideoCapture(file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            file_name = file.split('.')[0]
            fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

            print(fps, width, height, file_name, fourcc)
            return [fps, width, height, file_name, fourcc]
        else:
            return []

    def gen_file(self, path):
        """
        读取文件
        :param path:
        :return:
        """
        files_list = os.listdir(path)
        file_list = []
        for file in files_list:
            if not os.path.isdir(file):
                file_list.append(file)
        return file_list

    def create_video(self, videos_name, fourcc, fps, resolution):
        """
        创建视频
        :return:
        """
        # fourcc = cv2.VideoWriter_fourcc(*f'{self.fourcc}')
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        # FLV1编码体积更小
        file_list = os.listdir('./')
        v = cv2.VideoWriter(f'a/{videos_name}.mp4', fourcc, fps, resolution, True)
        for file in file_list:
            if file[-3:] == 'png':
                if file[0:-4] == videos_name:
                    for x in range(150):
                        img = cv2.imread(f'{file}')
                        v.write(img)


if __name__ == '__main__':
    v = Videos()
    # v.create_img(100, 200, text='这是测试')
    files = v.gen_file('./')
    for file in files:
        video_info = v.get_video_info(file)
        if video_info != []:
            # fps, width, height, file_name, fourcc
            v.create_img(video_info[1], video_info[2], video_info[3], "数字电子技术")
            v.create_video(videos_name=video_info[3], fourcc=video_info[4], fps=video_info[0],
                           resolution=(video_info[1], video_info[2]))
