# coding=utf8
import json
import os
import random

import itchat
import requests

from wxRobot import globalVars
from pic_extract import picExtract


REPLY_USER_NICKNAME = '冯泽明 付晓蕾 x X 安源 赵航'
REPLY_GROUPNAME = '叫啥叫啥！ 聊天机器人测试'


def get_response(msg):
    try:
        # 返回需要解码 [讲笑话的返回值特殊]
        r = requests.post(globalVars.get_apiUrl() + msg).content
        if '笑话' in msg:  # 注意 因为匹配关键词是 '笑话' 所以要用 in 判断是否存在于字符串中
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
    if msg['User'].NickName in REPLY_USER_NICKNAME:
        if '斗图' in msg['Text'].strip():
            doutu(msg)
        else:
            print('----给[' + msg['User'].NickName + ']的回复:' + (reply or defaultReply))
            return reply or defaultReply


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def bot_media_replay(msg):
    # 小胖子
    if msg['User'].NickName in REPLY_USER_NICKNAME:
        try:
            # 这里需要进行一场处理，否则可能因发送的图片为动态图造成程序异常中断
            pic_text = picExtract.get_file_text(msg['Text']())
            print(msg['User'].NickName + '想要斗图!' + pic_text)  # 加一条输出，后台确认发图片消息的人
            itchat.send_msg('你发的图片上写着：“' + pic_text + '”', msg['User'].UserName)
            # 识别图片上的文字，暂未指定处理方案
        except:
            print('{!@系统异常：#发送的图片未能处理,图片来自[' + msg['User'].NickName + ']}')
        doutu(msg)


@itchat.msg_register('Text', isGroupChat=True)
def group_reply(msg):
    text = msg['Text'].replace('@晓晓', '').strip()
    print(msg['ActualNickName'] + ' 说:' + text)
    defaultReply = ' “' + text + '”,朕已阅! '  # 容错，服务器无响应
    reply = get_response(text)  # @我的时候消息要特殊处理 && 指定的群进行特殊处理
    if msg['isAt'] or msg['User']['NickName'] in REPLY_GROUPNAME:
        if '斗图' in text:
            doutu(msg)
        else:
            print('----群[' + msg['User']['NickName'] + ']的回复:' + (reply or defaultReply))
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
    fileNumber = str(random.randint(0, globalVars.get_count())).zfill(2)  # zfill是python自带的补前置零函数
    fileName = globalVars.get_path() + '\\' + fileNumber
    if os.path.exists(fileName + '.jpg'):
        fileName += '.jpg'
    else:
        fileName += '.gif'
    print('\t[使用图片路径：' + fileName + ']\n')
    itchat.send_image(fileName, msg['User'].UserName)


if __name__ == '__main__':
    globalVars.set_path(os.path.abspath('.') + '\\doutu\\pictures')
    globalVars.set_count(maxCount())
    # 我们使用热启动,不用每次的都扫码登陆
    itchat.auto_login(hotReload=True)
    itchat.run()
