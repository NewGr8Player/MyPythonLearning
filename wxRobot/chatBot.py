# coding=utf8
import json
import os
import random

import itchat
import requests
import yaml

from wxRobot import globalVars


def get_config():  # 获取配置
    file = open(os.path.abspath('.') + "\\wxRobot\\config.yml")
    config = yaml.load(file)
    #
    baseUrl = 'http://i.itpk.cn/api.php'
    # API最大分析次数，取值范围为2-8，值越大精确率越高，但是会影响API响应时间
    limit = 'limit=' + config['config']['limit']
    api_key = 'api_key=' + config['config']['api_key']
    api_secret = 'api_secret=' + config['config']['api_secret']
    question = 'question='
    globalVars.set_apiUrl(baseUrl + '?' + limit + '&' + api_key + '&' + api_secret + '&' + question)


def get_response(msg):
    try:
        # 返回需要解码 [讲笑话的返回值特殊]
        r = requests.post(globalVars.get_apiUrl() + msg).content
        if '讲笑话' == msg:
            jsonStr = r.decode('utf-8-sig')
            jsonObj = json.loads(jsonStr)
            text = '《' + jsonObj['title'] + '》\n' + jsonObj['content']
            print(text)
            return text
        else:
            return r.decode('utf-8')
    except:
        return  # 将会返回一个None


@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def bot_reply(msg):
    text = msg['Text'].strip()
    print(msg['User'].NickName + ' 说:' + text)
    defaultReply = ' “' + text + '”,朕已阅! '  # 容错，服务器无响应
    reply = get_response(text)
    # 小胖子
    if msg['User'].NickName == '付晓蕾' or msg['User'].NickName == '冯泽明':
        if '斗图' == msg['Text'].strip():
            doutu(msg)
        else:
            return reply or defaultReply


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def bot_media_replay(msg):
    # 小胖子
    if msg['User'].NickName == '付晓蕾' or msg['User'].NickName == '冯泽明':
        doutu(msg)


@itchat.msg_register('Text', isGroupChat=True)
def group_reply(msg):
    text = msg['Text'].replace('@晓晓', '').strip()
    print(msg['ActualNickName'] + ' 说:' + text)
    defaultReply = ' “' + text + '”,朕已阅! '  # 容错，服务器无响应
    reply = get_response(text)  # @我的时候消息要特殊处理
    if msg['isAt']:
        if '斗图' == text:
            doutu(msg)
        else:
            return reply or defaultReply


def maxCount():
    number = 0
    for root, dirs, files in os.walk(globalVars.get_path()):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files) # 当前路径下所有非目录子文件
        for file in files:
            if int(file.split('.')[0]) > number:
                globalVars.set_count(int(file.split('.')[0]))
    return globalVars.get_count()


def doutu(msg):
    fileNumber = random.randint(0, globalVars.get_count())
    fileName = globalVars.get_path() + '\\' + str(fileNumber)
    if os.path.exists(fileName + '.jpg'):
        fileName += '.jpg'
    else:
        fileName += '.gif'
    itchat.send_image(fileName, msg['User'].UserName)


if __name__ == '__main__':
    globalVars.set_path(os.path.abspath('.') + '\\doutu\\pictures')
    globalVars.set_count(maxCount())
    # 获取配置
    get_config()
    # 我们使用热启动,不用每次的都扫码登陆
    itchat.auto_login(hotReload=True)
    itchat.run()
