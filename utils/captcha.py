# -*- coding: utf-8 -*-
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

fontType = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "font", "Arial.ttf")


def create_validate_code(size=(120, 30), chars=init_chars, mode="RGB", bg_color=(255, 255, 255), fg_color=(0, 0, 255),
                         font_size=18, font_type=fontType, length=4, draw_lines=True, n_line=(1, 2), draw_points=True,
                         point_chance=2):
    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)
    if draw_lines:
        create_lines(draw, n_line, width, height)
    if draw_points:
        create_points(draw, point_chance, width, height)
    strs = create_strs(draw, chars, length, font_type, font_size, width, height, fg_color)

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs


def create_lines(draw, n_line, width, height):
    line_num = random.randint(n_line[0], n_line[1])  # 干扰线条数
    for i in range(line_num):
        # 起始点
        begin = (random.randint(0, width), random.randint(0, height))
        # 结束点
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=(0, 0, 0))


def create_points(draw, point_chance, width, height):
    chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

    for w in range(width):
        for h in range(height):
            tmp = random.randint(0, 100)
            if tmp > 100 - chance:
                draw.point((w, h), fill=(0, 0, 0))


def create_strs(draw, chars, length, font_type, font_size, width, height, fg_color):
    c_chars = random.sample(chars, length)
    strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

    font = ImageFont.truetype(font_type, font_size)
    font_width, font_height = font.getsize(strs)

    draw.text(((width - font_width) / 3, (height - font_height) / 3), strs, font=font, fill=fg_color)

    return ''.join(c_chars)


def generate_verification_code():
    code_img, str_text = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'JPEG', quality=70)
    buf_str = buf.getvalue()
    return buf_str, str_text
