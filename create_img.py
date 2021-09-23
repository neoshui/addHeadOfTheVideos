import os
from PIL import Image, ImageDraw, ImageFont
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np



class Videos:
    def __init__(self):
        pass

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

    def walk_dir(self, root_path, file_list, dir_list):
        """
        遍历指定文件夹获取每一个文件路径
        :param root_path: 根目录
        :param file_list: 需保存的文件列表
        :param dir_list: 目录列表
        :return: 文件列表
        """
        file_or_dir = os.listdir(root_path)
        for file_dir in file_or_dir:
            file_dir_path = os.path.join(root_path, file_dir)
            if os.path.isdir(file_dir_path):
                dir_list.append(file_dir_path)
                self.walk_dir(file_dir_path, file_list, dir_list)
            else:
                file_list.append(file_dir_path)

        return file_list

        pass

    def get_video_info(self, file):
        """
        获取视频信息：fps,width,height,file_name
        :param file:视频文件路径
        :return: fps, width, height, file_name, fourcc, file_type, file_path
        """
        file_type = file.split('.')[-1]
        if len(file.split('/.')) == 1:
            if file_type == 'mp4' or file_type == 'MP4' or file_type == 'avi' or file_type == 'AVI' or file_type == 'mov' or file_type == 'MOV':
                # mov 和 mp4 格式兼容
                cap = cv2.VideoCapture(file)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                file_name = os.path.split(file)[1][0:-4]
                file_path = os.path.split(file)[0]

                fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

                # print(fps, width, height, file_name, fourcc)
                return [fps, width, height, file_name, fourcc, file_type, file_path]
            else:
                return []

    def create_img(self, width, height, title, logo_text, file_path):
        """
        创建背景图片
        :param width:视频宽度
        :param height:视频高度
        :param title:视频标题
        :param logo_text:logo文字
        :param file_path: 文件路径
        :return:
        """
        # old_new_img = Image.new('RGBA', (int(width), int(height)), color)
        origin_img = Image.open('background.png')
        new_img = origin_img.crop((0, 0, int(width), int(height)))
        self.draw_img(new_img, title, logo_text)
        new_img = self.add_img_logo(new_img, 'icon.png')
        new_img.save(f'{file_path}/{title}.png')
        pass

    def add_img_logo(self, new_img, icon):
        """
        粘贴logo图标
        :param new_img: 背景图片
        :param icon: logo
        :return: new_img
        """
        # img_size = new_img.size
        logo_img = Image.open(icon)
        new_img.paste(logo_img, (40, 40))
        return new_img

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
        # font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
        # font_path = fm.findfont(fm.FontProperties(family='wqy'))

        font_path = "STHeitiMedium.ttc"
        title_font_size = 100
        title_font = ImageFont.truetype(font_path, title_font_size)
        title_img_font_size = title_font.getsize(title_text)
        while title_img_font_size[0] > img_size[0]:
            title_font_size -= 5
            title_font = ImageFont.truetype(font_path, title_font_size)
            title_img_font_size = title_font.getsize(title_text)

        logo_font_size = 100
        logo_font = ImageFont.truetype(font_path, logo_font_size)
        logo_img_font_size = logo_font.getsize(logo_text)

        title_x = (img_size[0] - title_img_font_size[0]) / 2
        title_y = (img_size[1] - title_img_font_size[1]) / 2
        logo_x = (img_size[0] - (logo_img_font_size[0] + 30))
        logo_y = (img_size[1] - (logo_img_font_size[1] + 30))
        # print('img', img_size[0], img_size[1])
        # print('logo', logo_img_font_size[0], logo_img_font_size[1])
        # print('xy', logo_x, logo_y)

        # draw.text((title_x, title_y), title_text, font=title_font, fill="#1C1C1C")
        # draw.text((logo_x, logo_y), logo_text, font=title_font, fill="#1C1C1C")

        draw.text((title_x, title_y), title_text, font=title_font, fill="#1C1C1C")
        draw.text((logo_x, logo_y), logo_text, font=title_font, fill="#1C1C1C")

        pass

    def create_video(self, videos_name, fourcc, fps, resolution, videos_type, file_path):
        """
        创建视频
        :param videos_name: 视频名称
        :param fourcc: 编码
        :param fps: 帧率
        :param resolution: 分辨率
        :param videos_type: 文件类型
        :param file_path: 文件路径
        :return: create_file（文件是否创建成功）, videos_name, videos_type
        """
        # fourcc = cv2.VideoWriter_fourcc(*f'{self.fourcc}')
        create_file = False
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        # FLV1编码体积更小
        file_list = os.listdir(f'{file_path}/')
        v = cv2.VideoWriter(f'{file_path}/{videos_name}_h.{videos_type}', fourcc, fps, resolution, True)
        for file in file_list:
            if file[-3:] == 'png':
                if file[0:-4] == videos_name:
                    # img = cv2.imread(f'{file_path}/{file}')
                    img = cv2.imdecode(np.fromfile(f'{file_path}/{file}', dtype=np.uint8), -1)  # 解决上一条无法读取中文图片的问题
                    if img !=[]:
                        for x in range(150):
                            v.write(img)
                        create_file = True
                    else:
                        create_file = False
        return create_file, videos_name, videos_type

    def paste_videos(self, videos_name, videos_type, file_path):
        videos_list = []
        head = VideoFileClip(f'{file_path}/{videos_name}_h.{videos_type}')
        main = VideoFileClip(f'{file_path}/{videos_name}.{videos_type}')
        videos_list.append(head)
        videos_list.append(main)
        if videos_list != []:
            videos_clip = concatenate_videoclips(videos_list)
            videos_clip.to_videofile(f'{file_path}/{videos_name}_l.mp4')

    def mv_temp_file(self, file_name, file_type, file_path):
        os.remove(f'{file_path}/{file_name}_h.{file_type}')
        os.remove(f'{file_path}/{file_name}.png')

        pass


if __name__ == '__main__':
    v = Videos()
    files = v.walk_dir("./", [], [])

    for file in files:
        video_info = v.get_video_info(file)

        if video_info != None and video_info != []:
            # print(file, video_info)
            logo_name = video_info[6].split('/')[-1]
            print(logo_name)

            # fps, width, height, file_name, fourcc
            v.create_img(video_info[1], video_info[2], video_info[3], f'{logo_name}', video_info[6])

            create_file, videos_name, videos_type = v.create_video(videos_name=video_info[3], fourcc=video_info[4],
                                                                   fps=video_info[0],
                                                                   resolution=(video_info[1], video_info[2]),
                                                                   videos_type=video_info[5], file_path=video_info[6])
            if create_file:
                v.paste_videos(videos_name, videos_type, video_info[6])
                v.mv_temp_file(videos_name, videos_type, video_info[6])
