from PIL import Image,ImageEnhance
import pytesseract
from aip import AipOcr
import json

# file_path = '../doutu/pictures/02.jpg'
file_path = 'test.jpg'


def test():
    image = ImageEnhance.Contrast(Image.open(file_path).convert('L').point(lambda x: 0 if x < 143 else 255)).enhance(1.8)
    image.save('test1.jpg')
    text = pytesseract.image_to_string(image, lang='chi_sim').replace(' ', '')
    print(text)


# 定义常量
APP_ID = '9851066'
API_KEY = 'LUGBatgyRGoerR9FZbV4SQYk'
SECRET_KEY = 'fB2MNz1c2UHLTximFlC4laXPg7CVfyjV'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口
result = aipOcr.basicGeneral(get_file_content(file_path), options)
text1 = json.dumps(result['words_result'][0]['words'])
# .decode('unicode_escape')
# TODO 编码问题没解决！
print(text1)
