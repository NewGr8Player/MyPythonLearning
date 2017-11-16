# -*- coding:utf-8 -*-
# from PIL import Image, ImageEnhance
# import pytesseract
# import json

from aip import AipOcr
from wxRobot import globalVars


# FILE_PATH = '../doutu/pictures/03.jpg'
FILE_PATH = 'test1.jpg'


'''
# 测试本地文件
def test():
    image = ImageEnhance.Contrast(Image.open(file_path).convert('L').point(lambda x: 0 if x < 143 else 255)).enhance(1.8)
    image.save('test1.jpg')
    text = pytesseract.image_to_string(image, lang='chi_sim').replace(' ', '')
    print(text)
'''


# 初始化AipFace对象
aipOcr = AipOcr(globalVars.get_API_ID(), globalVars.get_API_KEY(), globalVars.get_SECRET_KEY())


# 文件配置
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# 调用通用文字识别接口
def get_file_text(file_stream):
    back = aipOcr.basicGeneral(file_stream, options)
    result = ''
    for text in back['words_result']:
        result += text['words']
    print("\t[图片识别结果：" + result + "]\n")
    return result
