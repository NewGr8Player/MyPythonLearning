import os
import yaml

global apiUrl
global count
global path
global APP_ID
global API_KEY
global SECRET_KEY


def set_apiUrl(value):
    global apiUrl
    apiUrl = value


def get_apiUrl():
    global apiUrl
    return apiUrl


def get_count():
    global count
    return count


def set_count(value):
    global count
    count = value


def set_path(value):
    global path
    path = value


def get_path():
    global path
    return path


def set_APP_ID(value):
    global APP_ID
    APP_ID = value


def get_API_ID():
    global APP_ID
    return APP_ID


def set_API_KEY(value):
    global API_KEY
    API_KEY = value


def get_API_KEY():
    global API_KEY
    return API_KEY


def set_SECRET_KEY(value):
    global SECRET_KEY
    SECRET_KEY = value


def get_SECRET_KEY():
    global SECRET_KEY
    return SECRET_KEY


def init():
    file = open(os.path.abspath('.') + "\\wxRobot\\config.yml")
    config = yaml.load(file)
    config_root = config['config']
    robot_api = config_root['robot_api']
    baseUrl = 'http://i.itpk.cn/api.php'
    # API最大分析次数，取值范围为2-8，值越大精确率越高，但是会影响API响应时间
    limit = 'limit=' + robot_api['limit']
    api_key = 'api_key=' + robot_api['api_key']
    api_secret = 'api_secret=' + robot_api['api_secret']
    question = 'question='
    set_apiUrl(baseUrl + '?' + limit + '&' + api_key + '&' + api_secret + '&' + question)
    baidu_api = config_root['baidu_api']
    set_APP_ID(baidu_api['api_id'])
    set_API_KEY(baidu_api['api_key'])
    set_SECRET_KEY(baidu_api['secret_key'])


# 调用初始化函数
init()
